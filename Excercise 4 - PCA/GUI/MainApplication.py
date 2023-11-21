import tkinter as tk
from PIL import Image, ImageTk


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title("PCA")
        self.parent.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        # Tạo cột trái
        left_frame = tk.Frame(self)
        left_frame.pack(side="left", fill="y")

        browser_button = tk.Button(left_frame, text="Browser", command=self.browse)
        browser_button.pack(pady=10)

        save_button = tk.Button(left_frame, text="Save", command=self.save)
        save_button.pack(side="bottom", pady=10)

        quit_button = tk.Button(left_frame, text="Quit", command=self.parent.destroy)
        quit_button.pack(side="bottom", pady=10)

        # Tạo cột phải
        right_frame = tk.Frame(self)
        right_frame.pack(side="right", fill="both", expand=True)

        title_label = tk.Label(right_frame, text="Image Viewer", font=("Arial", 18))
        title_label.pack(pady=20)

        # Tạo frame chứa các ảnh
        image_frame = tk.Frame(right_frame)
        image_frame.pack()

        image1_label = tk.Label(image_frame)
        image1_label.grid(row=0, column=0, padx=10, pady=5)
        image2_label = tk.Label(image_frame)
        image2_label.grid(row=0, column=1, padx=10, pady=5)
        image3_label = tk.Label(image_frame)
        image3_label.grid(row=0, column=2, padx=10, pady=5)

    def browse(self):
        # Viết hàm xử lý khi nhấn nút Browser để mở ảnh

        # Tạo dialog mở file và xử lý việc chọn ảnh
        pass

    def save(self):
        # Viết hàm xử lý khi nhấn nút Save để lưu ảnh

        # Lưu ảnh
        pass
