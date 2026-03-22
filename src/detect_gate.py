import cv2
import os
import numpy as np

folder = "/home/amrutha/amrutha/gate_test/resized"
output_folder = "/home/amrutha/amrutha/gate_test/output"
os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(folder):
    path = os.path.join(folder, file)

    img = cv2.imread(path)
    if img is None:
        continue

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 🎯 Detect RED color (you can tune later)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2

    # Clean noise
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centers = []

    for cnt in contours:
        area = cv2.contourArea(cnt)

        if area > 500:  # filter noise
            x, y, w, h = cv2.boundingRect(cnt)

            # 🎯 Filter vertical shapes (gate poles)
            if h > w:  
                cx = x + w // 2
                cy = y + h // 2
                centers.append((cx, cy))

                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

    # 🎯 If we detect 2 poles → compute center
    if len(centers) >= 2:
        avg_x = sum([c[0] for c in centers]) // len(centers)
        avg_y = sum([c[1] for c in centers]) // len(centers)

        cv2.circle(img, (avg_x, avg_y), 6, (0,0,255), -1)
        print(f"{file} → Gate Center: ({avg_x}, {avg_y})")
    else:
        print(f"{file} → ⚠️ Gate NOT detected")

    cv2.imwrite(os.path.join(output_folder, file), img)

    cv2.imshow("Detection", img)
    cv2.waitKey(100)

cv2.destroyAllWindows()
