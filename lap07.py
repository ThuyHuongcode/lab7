import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os

# ===============================
# ẢNH ĐẦU VÀO
# ===============================
INPUT_FILENAME = "cameraman.tif"   # tên file ảnh thật
OUTPUT_DIR = "rlc_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 1. Đọc ảnh thật ---
img = Image.open(INPUT_FILENAME).convert("L")  # "L" = ảnh xám (0..255)
image = np.array(img, dtype=np.uint8)

# --- 2. (Tùy chọn) Giảm kích thước ảnh cho nhanh ---
# (bạn có thể tắt nếu muốn ảnh gốc)
img_small = img.resize((256, 256), Image.BILINEAR)
image = np.array(img_small, dtype=np.uint8)

# --- 3. (Tùy chọn) Chuyển ảnh sang đen trắng 0/255 (để RLC hiệu quả hơn) ---
THRESHOLD = 128
image_bw = np.where(image >= THRESHOLD, 255, 0).astype(np.uint8)

# Lưu ảnh sau khi xử lý đầu vào
Image.fromarray(image_bw).save(os.path.join(OUTPUT_DIR, "prepared_image.png"))

# --- 4. Hiển thị ảnh ban đầu ---
plt.imshow(image_bw, cmap='gray', vmin=0, vmax=255)
plt.title("Ảnh Cameraman (đen trắng)")
plt.axis('off')
plt.show()

# --- 5. Hàm mã hóa Run-Length Coding ---
def rle_encode(img_array):
    flat = img_array.flatten()
    encoded = []
    if flat.size == 0:
        return encoded
    count = 1
    prev = flat[0]
    for val in flat[1:]:
        if val == prev:
            count += 1
        else:
            encoded.append((int(prev), int(count)))
            prev = val
            count = 1
    encoded.append((int(prev), int(count)))
    return encoded

# --- 6. Hàm giải mã ---
def rle_decode(encoded_list, shape):
    flat = []
    for value, count in encoded_list:
        flat.extend([value] * count)
    return np.array(flat, dtype=np.uint8).reshape(shape)

# --- 7. Thực hiện mã hóa và giải mã ---
encoded = rle_encode(image_bw)
decoded = rle_decode(encoded, image_bw.shape)

# --- 8. Hiển thị ảnh sau khi giải mã ---
plt.imshow(decoded, cmap='gray', vmin=0, vmax=255)
plt.title("Ảnh sau khi giải mã RLC (giống ảnh gốc)")
plt.axis('off')
plt.show()

# --- 9. Lưu ảnh giải mã ---
decoded_path = os.path.join(OUTPUT_DIR, "decoded_image.png")
Image.fromarray(decoded).save(decoded_path)

# --- 10. Lưu dữ liệu RLE ra file văn bản ---
rle_txt = os.path.join(OUTPUT_DIR, "encoded_rle.txt")
with open(rle_txt, "w") as f:
    for val, cnt in encoded:
        f.write(f"{val},{cnt}\n")

# --- 11. Thống kê ---
total_pixels = image_bw.size
num_runs = len(encoded)
compression_ratio = round(num_runs * 2 / total_pixels, 4)

print("Ảnh đầu vào:", INPUT_FILENAME)
print("Kích thước ảnh:", image_bw.shape)
print("Tổng số pixel:", total_pixels)
print("Số run sau khi RLC:", num_runs)
print("Tỉ lệ nén (≈ RLE/Raw):", compression_ratio)
print("Ảnh đen trắng lưu tại:", os.path.join(OUTPUT_DIR, "prepared_image.png"))
print("Ảnh giải mã lưu tại:", decoded_path)
print("File RLE lưu tại:", rle_txt)
