import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from PCA import PCA
from utils import *
import os

images = []
flatten_images = []
reconstructed_images = []
shown_image_index = 0


class LeftSideBar(ttk.Frame):
    def __init__(self, container, bg_color="pink"):
        super().__init__(container)
        self.container = container
        self.path = None

        self.width = 100
        self.configure(width=self.width)  # Set width to 100

        # Create a custom style for the left sidebar
        self.bg = bg_color
        self.style = ttk.Style()
        self.style.configure("LeftSide.TFrame", background=bg_color)

        # Apply the custom style to the frame
        self.configure(style="LeftSide.TFrame")

        self.__create_widgets()

    def __create_widgets(self):
        # Nút Browser
        ttk.Button(self, text="Load dataset", command=self.load_dataset).pack(
            anchor=tk.W, padx=5, pady=(5, 15), fill=tk.X
        )

        # Frame to hold Radiobuttons and corresponding Spinboxes
        radio_frame = tk.Frame(self)
        radio_frame.pack(anchor=tk.W, padx=5)

        self.selection = tk.IntVar()
        self.selection.set(1)  # Set default selection to No. PCs

        def on_radio_selection():
            selected = self.selection.get()
            if selected == 1:
                self.n_pc_spinbox.configure(state="normal")
                self.preserved_var_spinbox.configure(state="disabled")
            elif selected == 2:
                self.n_pc_spinbox.configure(state="disabled")
                self.preserved_var_spinbox.configure(state="normal")

        tk.Radiobutton(
            radio_frame,
            text="No. PCs",
            variable=self.selection,
            value=1,
            command=on_radio_selection,
        ).pack(pady=5, anchor="w")

        self.n_pc_var = tk.StringVar(value="30")
        self.n_pc_spinbox = ttk.Spinbox(
            radio_frame, from_=0, to=100, textvariable=self.n_pc_var
        )
        self.n_pc_spinbox.pack(pady=5)

        tk.Radiobutton(
            radio_frame,
            text="Preserved variance (%)",
            variable=self.selection,
            value=2,
            command=on_radio_selection,
        ).pack(pady=5, anchor="w")

        self.preserved_var_var = tk.StringVar(value="95")
        self.preserved_var_spinbox = ttk.Spinbox(
            radio_frame, from_=0, to=100, textvariable=self.preserved_var_var
        )
        self.preserved_var_spinbox.pack(pady=5)

        # Button Run
        ttk.Button(self, text="Run", command=self.handle_run).pack(
            anchor=tk.W, padx=5, pady=(25, 0), fill=tk.X
        )

        # Button Save và Button Quit
        ttk.Button(self, text="Quit", command=self.container.close_app).pack(
            side=tk.BOTTOM, padx=5, pady=5, fill=tk.X
        )
        ttk.Button(self, text="Save", command=self.container.save).pack(
            side=tk.BOTTOM, padx=5, pady=5, fill=tk.X
        )

        # Initial setup to disable one of the Spinbox
        self.n_pc_spinbox.configure(state="normal")
        self.preserved_var_spinbox.configure(state="disabled")

    def load_dataset(self):
        self.path = filedialog.askdirectory()
        if self.path:
            self.container.handle_load_dataset(self.path)

    def handle_run(self):
        if not self.path:
            # thông báo lỗi chưa chọn dataset
            messagebox.showerror("Error", "Please load a dataset first.")
            return

        selected = self.selection.get()
        if selected == 1:
            try:
                num_components = int(self.n_pc_var.get())
                if num_components <= 0 or num_components > 200:
                    messagebox.showerror(
                        "Error",
                        "Invalid value for No. PCs. Please enter a value between 1 and 200.",
                    )
            except ValueError:
                messagebox.showerror(
                    "Error", "Invalid value for No. PCs. Please enter a valid number."
                )
                return

            self.container.run_pca(
                num_components=num_components, preserved_variance=None
            )
        elif selected == 2:
            try:
                preserved_variance = float(self.preserved_var_var.get())
                if preserved_variance <= 0 or preserved_variance > 100:
                    messagebox.showerror(
                        "Error",
                        "Invalid value for Preserved variance. Please enter a value between 0 and 100.",
                    )
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Invalid value for Preserved variance. Please enter a valid number.",
                )
                return

            self.container.run_pca(
                num_components=None, preserved_variance=preserved_variance
            )


class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        self.columnconfigure(0, weight=1)
        self.__create_widgets()

    def __create_widgets(self):
        # Main title
        main_title = tk.Label(
            self,
            text="PCA for image dimensionality reduction",
            font=("Arial", 16, "bold"),
        )
        main_title.grid(row=0, column=0, pady=(20, 10), sticky="n")

        # Tạo frame chứa label và spinbox cho image index
        image_index_frame = tk.Frame(self)
        image_index_frame.grid(row=1, column=0, pady=(0, 20))

        self.image_index_label = tk.Label(
            image_index_frame, font=("Arial", 10), text="Image Index:"
        )
        self.image_index_label.pack(side=tk.LEFT)

        self.image_index_var = tk.StringVar(value="1")
        self.image_index_spinbox = ttk.Spinbox(
            image_index_frame,
            from_=1,
            to=len(images),
            textvariable=self.image_index_var,
            command=self.update_image_by_index,
        )
        self.image_index_spinbox.configure(state="disabled")
        self.image_index_spinbox.pack(side=tk.LEFT, padx=5)

        # Frame to hold 2 images in a row
        images_row_frame = ttk.Frame(self)
        images_row_frame.grid(row=2, column=0, pady=(20, 10))

        # Input Image Frame
        input_frame = tk.Frame(images_row_frame)
        input_frame.grid(row=0, column=0, padx=10)

        # Reconstruction Image Frame
        reconstruction_frame = tk.Frame(images_row_frame)
        reconstruction_frame.grid(row=0, column=1, padx=10)

        tk.Label(input_frame, text="Input Image", font=("Arial", 12, "bold")).pack()
        tk.Label(
            reconstruction_frame,
            text="Reconstruction",
            font=("Arial", 12, "bold"),
        ).pack()

        self.input_image = tk.Label(input_frame)
        self.input_image.pack(side=BOTTOM)
        self.reconstructed_image = tk.Label(reconstruction_frame)
        self.reconstructed_image.pack(side=BOTTOM)

    def update_input_image(self, image):
        # Chuyển đổi mảng NumPy thành hình ảnh của Pillow
        pil_image = Image.fromarray(image)
        # Resize hình ảnh
        pil_image_resized = pil_image.resize((200, 200), Image.ANTIALIAS)
        # Chuyển đổi hình ảnh của Pillow thành ImageTk để hiển thị trong khung hình Tkinter
        photo = ImageTk.PhotoImage(pil_image_resized)
        self.input_image.configure(image=photo)
        self.input_image.image = photo

    def update_reconstructed_image(self, image):
        # Chuyển đổi mảng NumPy thành hình ảnh của Pillow
        pil_image = Image.fromarray(image)
        # Resize hình ảnh
        pil_image_resized = pil_image.resize((200, 200), Image.ANTIALIAS)
        # Chuyển đổi hình ảnh của Pillow thành ImageTk để hiển thị trong khung hình Tkinter
        photo = ImageTk.PhotoImage(pil_image_resized)
        self.reconstructed_image.configure(image=photo)
        self.reconstructed_image.image = photo

    def update_image_by_index(self):
        print(len(images))
        shown_image_index = int(self.image_index_var.get())
        if 0 <= shown_image_index < len(images):
            self.update_input_image(images[shown_image_index])
        if 0 <= shown_image_index < len(reconstructed_images):
            self.update_reconstructed_image(reconstructed_images[shown_image_index])

    def update_image_spinbox_range(self, max_index):
        # max_index = len(images)
        self.image_index_spinbox.configure(to=max_index)
        self.image_index_var.set("1")
        if max_index <= 0:
            self.image_index_spinbox.configure(state="disabled")
        else:
            self.image_index_spinbox.configure(state="active")


class App(tk.Tk):
    def __init__(self, title, geo):
        super().__init__()

        self.pca = PCA()

        self.title(title)
        self.geometry(geo)
        self.resizable(0, 0)

        # layout on the root window
        self.columnconfigure(0, weight=0)  # Avoid weight conflicts
        self.columnconfigure(1, weight=1)

        self.__create_widgets()

    def __create_widgets(self):
        # create the left side bar
        self.left_side_bar = LeftSideBar(self)
        self.left_side_bar.pack(side=tk.LEFT, fill=tk.Y)

        # create the main frame
        self.right_side_bar = MainFrame(self)
        self.right_side_bar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def handle_load_dataset(self, path):
        # Khi người dùng đã chọn dataset mới thì tiến hành load ảnh lên, tiền xử lý và fit pca
        global images, flatten_images
        # del images  # giải phóng bộ nhớ
        # del flatten_images
        images, flatten_images = load_and_preprocess_dataset(path)
        # print(len(images))
        # print(flatten_images.shape)
        # Cập nhật số lượng ảnh ở spinbox
        self.right_side_bar.update_image_spinbox_range(len(images))

        if images:
            # load thành công
            self.right_side_bar.update_input_image(
                images[shown_image_index]
            )  # cập nhật ảnh hiển thị
            del self.pca  # Giải phóng bộ nhớ
            self.pca = PCA()  # Tạo instance mới
            (self.Xbar, self.mu, _) = self.pca.standardize(flatten_images)  # chuẩn hóa
            num_components = int(self.left_side_bar.n_pc_var.get())
            if num_components <= self.Xbar.shape[1]:
                self.pca.optimize = True
            self.pca.fit(self.Xbar)

        else:
            messagebox.showerror("Error", "Can't load this dataset!")
            return

    def close_app(self):
        self.destroy()

    def save(self):
        print("TODO")

    def run_pca(self, num_components, preserved_variance):
        global reconstructed_images
        # Chạy lại ảnh khôi phục
        reconstructed_images = self.pca.reconstruct_img(
            self.Xbar, self.mu, num_components, preserved_variance
        )
        # error = mse(reconstructed_imgs, Xbar)

        # Update ảnh lên main frame
        self.right_side_bar.update_reconstructed_image(
            reconstructed_images[shown_image_index]
        )


if __name__ == "__main__":
    title = "PCA Demo"
    geo = "1200x640"
    app = App(title, geo)
    app.mainloop()
