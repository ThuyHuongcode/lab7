
# Demo RLC với giao diện tkinter
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from rlc_logic import open_and_prepare_image, rle_encode, rle_decode, get_compression_info

class RLCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Demo Nén Ảnh RLC với Tkinter")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)

        self.img_path = None
        self.img_goc = None
        self.img_gray = None
        self.img_bw = None
        self.img_decoded = None
        self.encoded = None

        # Frames
        self.frame_top = tk.Frame(root)
        self.frame_top.pack(pady=10)
        self.frame_mid = tk.Frame(root)
        self.frame_mid.pack()
        self.frame_info = tk.Frame(root)
        self.frame_info.pack(pady=10)

        # Nút tải ảnh
        self.btn_load = tk.Button(self.frame_top, text="Tải ảnh", command=self.load_image, font=("Arial", 12))
        self.btn_load.pack()

        # Canvas hiển thị ảnh
        self.canvas_goc = tk.Canvas(self.frame_mid, width=256, height=256, bg="white")
        self.canvas_goc.grid(row=0, column=0, padx=10)
        self.canvas_bw = tk.Canvas(self.frame_mid, width=256, height=256, bg="white")
        self.canvas_bw.grid(row=0, column=1, padx=10)
        self.canvas_decoded = tk.Canvas(self.frame_mid, width=256, height=256, bg="white")
        self.canvas_decoded.grid(row=0, column=2, padx=10)

        tk.Label(self.frame_mid, text="Ảnh gốc", font=("Arial", 11)).grid(row=1, column=0)
        tk.Label(self.frame_mid, text="Ảnh nén (đen trắng)", font=("Arial", 11)).grid(row=1, column=1)
        tk.Label(self.frame_mid, text="Ảnh giải mã", font=("Arial", 11)).grid(row=1, column=2)

        # Thông tin nén
        self.info_text = tk.Text(self.frame_info, width=90, height=8, font=("Consolas", 11))
        self.info_text.pack()
        self.info_text.config(state=tk.DISABLED)

    def load_image(self):
        filetypes = [("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff")]
        path = filedialog.askopenfilename(title="Chọn ảnh để nén", filetypes=filetypes)
        if not path:
            return
        self.img_path = path
        try:
            img, arr_bw, img_bw = open_and_prepare_image(path)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không mở được ảnh: {e}")
            return
        self.img_goc = img
        self.img_bw = img_bw
        self.encoded = rle_encode(arr_bw)
        arr_decoded = rle_decode(self.encoded, arr_bw.shape)
        self.img_decoded = Image.fromarray(arr_decoded)
        self.show_images()
        self.show_info(arr_bw)

    def show_images(self):
        # Ảnh gốc
        img_goc_tk = ImageTk.PhotoImage(self.img_goc)
        self.canvas_goc.img = img_goc_tk
        self.canvas_goc.create_image(0, 0, anchor=tk.NW, image=img_goc_tk)
        # Ảnh nén (đen trắng)
        img_bw_tk = ImageTk.PhotoImage(self.img_bw)
        self.canvas_bw.img = img_bw_tk
        self.canvas_bw.create_image(0, 0, anchor=tk.NW, image=img_bw_tk)
        # Ảnh giải mã
        img_decoded_tk = ImageTk.PhotoImage(self.img_decoded)
        self.canvas_decoded.img = img_decoded_tk
        self.canvas_decoded.create_image(0, 0, anchor=tk.NW, image=img_decoded_tk)

    def show_info(self, arr_bw):
        info = get_compression_info(arr_bw, self.encoded, self.img_path)
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, info)
        self.info_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = RLCApp(root)
    root.mainloop()
