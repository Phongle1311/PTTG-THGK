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
        # self.n_pc_spinbox.delete(0, "end")
        # self.n_pc_spinbox.insert(0, "30")
        self.n_pc_spinbox.pack(pady=5)

        tk.Radiobutton(
            radio_frame,
            text="Preserved variance",
            variable=self.selection,
            value=2,
            command=on_radio_selection,
        ).pack(pady=5, anchor="w")

        self.preserved_var_var = tk.StringVar(value="95")
        self.preserved_var_spinbox = ttk.Spinbox(
            radio_frame, from_=0, to=100, textvariable=self.preserved_var_var
        )
        # self.preserved_var_spinbox.delete(0, "end")
        # self.preserved_var_spinbox.insert(0, "95")
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
        self.container.handle_load_dataset(self.path)

    def handle_run(self):
        if self.path is None:
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

        # Frame to hold 2 images in a row
        images_row_frame = ttk.Frame(self)
        images_row_frame.grid(row=1, column=0, pady=(20, 10))

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


class App(tk.Tk):
    def __init__(self, title, geo):
        super().__init__()
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
        images, flatten_images = load_and_preprocess_dataset(path)
        if images:
            # load thành công
            self.right_side_bar.update_input_image(images[shown_image_index])
            pass
        else:
            # load thất bại/không hợp lệ
            # thông báo lỗi
            pass

    def close_app(self):
        self.destroy()

    def save(self):
        print("TODO")

    def run_pca(self, num_components, preserved_variance):
        if num_components == None:
            # tính num_pc dựa vào preserved var
            pass
        pca = PCA()
        Xbar, mu, std = pca.standardize(flatten_images)
        pca.fit(Xbar)
        reconstructed_imgs = pca.reconstruct_img(Xbar, num_components)
        error = mse(reconstructed_imgs, Xbar)

    # def run_pca(self):
    #     if self.image_folder:
    #         # Load ảnh đầu tiên
    #         image_list = os.listdir(self.image_folder)
    #         if image_list:
    #             image_path = os.path.join(self.image_folder, image_list[0])
    #             original_image = Image.open(image_path)

    #             # Thực hiện PCA
    #             pca = PCA()

    #             # Chuyển đổi ảnh thành dạng phù hợp cho PCA (numpy array)
    #             image_array = np.array(original_image)
    #             # Reshape ảnh (nếu cần)

    #             # Tiến hành chuẩn hóa và giảm chiều
    #             processed_image, mu, std = pca.standardize(image_array)
    #             pca.fit(processed_image)
    #             num_components = int(n_pc_var.get())  # Lấy số chiều từ spinbox
    #             reduced_image = pca.reconstruct_img(processed_image, num_components)

    #             # Tái tạo ảnh từ kết quả giảm chiều
    #             reconstructed_image = pca.reconstruct_img(reduced_image, num_components)

    #             # Hiển thị ảnh gốc, sau khi giảm chiều và tái tạo
    #             self.display_image(original_image, 0)
    #             self.display_image(reduced_image, 1)
    #             self.display_image(reconstructed_image, 2)


if __name__ == "__main__":
    title = "PCA Demo"
    geo = "1200x640"
    app = App(title, geo)
    app.mainloop()
