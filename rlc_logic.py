import numpy as np
from PIL import Image
import os

def open_and_prepare_image(path, size=(256, 256), threshold=128):
    """
    Đọc ảnh, chuyển sang xám, resize, chuyển sang đen trắng 0/255
    Trả về: img_goc (PIL), arr_bw (numpy array), img_bw (PIL)
    """
    img = Image.open(path).convert("L")
    img = img.resize(size, Image.BILINEAR)
    arr = np.array(img, dtype=np.uint8)
    arr_bw = np.where(arr >= threshold, 255, 0).astype(np.uint8)
    img_bw = Image.fromarray(arr_bw)
    return img, arr_bw, img_bw

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

def rle_decode(encoded_list, shape):
    flat = []
    for value, count in encoded_list:
        flat.extend([value] * count)
    return np.array(flat, dtype=np.uint8).reshape(shape)

def get_compression_info(arr_bw, encoded, img_path):
    total_pixels = arr_bw.size
    num_runs = len(encoded)
    n_data = num_runs * 2
    compression_ratio = round(n_data / total_pixels, 4)
    h, w = arr_bw.shape
    info = (
        f"THÔNG TIN NÉN ẢNH BẰNG RLC\n"
        f"-----------------------------\n"
        f"Tên file ảnh đầu vào: {os.path.basename(img_path)}\n"
        f"Kích thước ảnh: {h} x {w} (cao x rộng)\n"
        f"Tổng số pixel: {total_pixels}\n"
        f"Số run sau khi nén: {num_runs}\n"
        f"Số phần tử dữ liệu sau nén (run x 2): {n_data}\n"
        f"Tỉ lệ nén (số phần tử nén / tổng pixel): {compression_ratio}\n"
        f"\nGhi chú: Ảnh nén là ảnh đen trắng 0/255 để RLC hiệu quả hơn.\n"
    )
    return info
