import cv2
import os

folder = "/home/amrutha/amrutha/gate_test/images"

valid_count = 0
corrupt_count = 0

print("🔍 Checking images...\n")

for file in os.listdir(folder):
    path = os.path.join(folder, file)

    # Skip non-image files
    if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
        print(f"⚠️ Skipped (not image): {file}")
        continue

    img = cv2.imread(path)

    if img is None:
        print(f"❌ Corrupted: {file}")
        corrupt_count += 1
    else:
        h, w, c = img.shape
        print(f"✅ OK: {file} | Shape: {h}x{w}x{c}")
        valid_count += 1

        # Show image briefly
        cv2.imshow("Preview", img)
        cv2.waitKey(100)

cv2.destroyAllWindows()

print("\n📊 Summary:")
print(f"Valid images: {valid_count}")
print(f"Corrupted images: {corrupt_count}")
