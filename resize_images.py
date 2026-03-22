import cv2
import os

input_folder = "/home/amrutha/amrutha/gate_test/images"
output_folder = "/home/amrutha/amrutha/gate_test/resized"

os.makedirs(output_folder, exist_ok=True)

TARGET_SIZE = (640, 480)  # width, height

for file in os.listdir(input_folder):
    path = os.path.join(input_folder, file)

    if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    img = cv2.imread(path)

    if img is None:
        continue

    resized = cv2.resize(img, TARGET_SIZE)

    save_path = os.path.join(output_folder, file)
    cv2.imwrite(save_path, resized)

    print(f"✅ Resized: {file}")

print("\n🎯 All images resized to 640x480")

