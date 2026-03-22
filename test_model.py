from ultralytics import YOLO
import cv2
import os

# Load trained model
model = YOLO("/home/amrutha/rov_ws/runs/detect/train/weights/best.pt")

# Folder containing test images
folder = "/home/amrutha/amrutha/gate_test/resized"

# Control gain
k = 0.002

for file in os.listdir(folder):
    img_path = os.path.join(folder, file)

    img = cv2.imread(img_path)
    if img is None:
        continue

    results = model(img)

    h, w = img.shape[:2]

    # Draw image center (reference)
    cv2.circle(img, (w//2, h//2), 6, (255, 0, 0), -1)  # Blue dot

    for r in results:
        boxes = r.boxes

        if boxes is not None and len(boxes) > 0:

            # 🔥 Choose largest bounding box (main gate)
            largest_box = max(
                boxes,
                key=lambda b: (b.xyxy[0][2] - b.xyxy[0][0]) *
                              (b.xyxy[0][3] - b.xyxy[0][1])
            )

            x1, y1, x2, y2 = map(int, largest_box.xyxy[0])

            # Draw bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Compute center
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            # Draw detected center
            cv2.circle(img, (center_x, center_y), 6, (0, 0, 255), -1)  # Red dot

            print(f"{file} → Center: ({center_x}, {center_y})")

            # 🔥 IBVS ERROR
            error_x = center_x - (w // 2)
            error_y = center_y - (h // 2)

            print(f"Error: ({error_x}, {error_y})")

            # 🔥 CONTROL (Proportional)
            vx = -k * error_x
            vy = -k * error_y

            print(f"Control → vx: {vx:.3f}, vy: {vy:.3f}")

        else:
            print(f"{file} → ❌ No gate detected")

    cv2.imshow("IBVS Detection", img)
    cv2.waitKey(100)

cv2.destroyAllWindows()
