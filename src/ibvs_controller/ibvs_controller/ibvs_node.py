import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from ultralytics import YOLO
import cv2
import os

class IBVSNode(Node):

    def __init__(self):
        super().__init__('ibvs_node')

        # Publisher
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        # Load trained YOLO model
        self.model = YOLO('/home/amrutha/rov_ws/runs/detect/train/weights/best.pt')

        # Input images
        self.image_folder = "/home/amrutha/amrutha/gate_test/resized"
        self.image_list = sorted(os.listdir(self.image_folder))
        self.index = 0

        # Output folder
        self.output_folder = "/home/amrutha/rov_ws/output"
        os.makedirs(self.output_folder, exist_ok=True)

        # Timer
        self.timer = self.create_timer(0.5, self.process_frame)

        # IBVS parameters
        self.k = 0.002
        self.threshold = 30

    def process_frame(self):

        # Stop after all images
        if self.index >= len(self.image_list):
            self.get_logger().info("✅ Finished dataset. Shutting down...")
            rclpy.shutdown()
            return

        filename = self.image_list[self.index]
        img_path = os.path.join(self.image_folder, filename)
        self.index += 1

        frame = cv2.imread(img_path)
        if frame is None:
            return

        results = self.model(frame)

        h, w = frame.shape[:2]

        # Draw image center (BLUE)
        cv2.circle(frame, (w//2, h//2), 6, (255, 0, 0), -1)

        twist = Twist()

        gate_detected = False   # 🔥 KEY FLAG

        for r in results:
            boxes = r.boxes

            if boxes is not None and len(boxes) > 0:
                gate_detected = True

                # Pick largest gate
                largest_box = max(
                    boxes,
                    key=lambda b: (b.xyxy[0][2] - b.xyxy[0][0]) *
                                  (b.xyxy[0][3] - b.xyxy[0][1])
                )

                x1, y1, x2, y2 = map(int, largest_box.xyxy[0])

                # Draw box
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # Gate center (RED)
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                cv2.circle(frame, (center_x, center_y), 6, (0, 0, 255), -1)

                # Error
                error_x = center_x - (w // 2)
                error_y = center_y - (h // 2)

                # 🔥 DECISION: IBVS CONTROL
                if abs(error_x) < self.threshold and abs(error_y) < self.threshold:
                    # Aligned → go forward (pass through gate)
                    twist.linear.x = 0.3
                    self.get_logger().info(f"{filename} → 🚀 FORWARD (Aligned)")

                else:
                    # Not aligned → IBVS correction
                    vx = -self.k * error_x
                    vy = -self.k * error_y

                    twist.linear.x = vx
                    twist.linear.y = vy

                    self.get_logger().info(
                        f"{filename} → 🎯 ALIGN | vx: {vx:.3f}, vy: {vy:.3f}"
                    )

        # 🔥 FALLBACK (NO GATE DETECTED)
        if not gate_detected:
            twist.angular.z = 0.2  # rotate to search
            self.get_logger().info(f"{filename} → 🔍 SEARCHING...")

        # Save output image
        output_path = os.path.join(self.output_folder, filename)
        cv2.imwrite(output_path, frame)

        # Publish command
        self.publisher.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    node = IBVSNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
