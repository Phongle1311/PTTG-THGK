import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from PCA import PCA
from utils import *
import os

images = []
flatten_images = []


class LeftSideBar(ttk.Frame):
    def __init__(self, container, bg_color="pink"):
        super().__init__(container)
        self.container = container

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

        # Label và Spinbox cho no. principle components
        label_n_pc = tk.Label(self, text="No. PCs", bg=self.bg)
        label_n_pc.pack(anchor=tk.W, padx=5)
        n_pc_var = tk.StringVar()
        n_pc_spinbox = ttk.Spinbox(self, from_=0, to=100, textvariable=n_pc_var)
        n_pc_spinbox.pack(anchor=tk.W, padx=5, fill=tk.X)

        # Label và Spinbox cho preserved variance
        label_preserved_var = tk.Label(self, text="Preserved variance", bg=self.bg)
        label_preserved_var.pack(anchor=tk.W, padx=5)
        preserved_var_var = tk.StringVar()
        preserved_var_spinbox = ttk.Spinbox(
            self, from_=0, to=100, textvariable=preserved_var_var
        )
        preserved_var_spinbox.pack(anchor=tk.W, padx=5, fill=tk.X)

        # Button Run
        ttk.Button(self, text="Run").pack(anchor=tk.W, padx=5, pady=(25, 0), fill=tk.X)

        # Button Save và Button Quit
        ttk.Button(self, text="Quit").pack(side=BOTTOM, padx=5, pady=5, fill=tk.X)
        ttk.Button(self, text="Save").pack(side=BOTTOM, padx=5, pady=5, fill=tk.X)

    def load_dataset(self):
        path = filedialog.askdirectory()
        self.container.handle_load_dataset(path)


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

        # Frame to hold three images in a row
        images_row_frame = ttk.Frame(self)
        images_row_frame.grid(row=1, column=0, pady=(0, 10))

        # Before Image Frame
        before_frame = ttk.Frame(images_row_frame)
        before_frame.grid(row=0, column=0, padx=10)
        label_before = tk.Label(before_frame, text="Before", font=("Arial", 12, "bold"))
        label_before.pack()
        # Add your before image display widget here

        # After Image Frame
        after_frame = ttk.Frame(images_row_frame)
        after_frame.grid(row=0, column=1, padx=10)
        label_after = tk.Label(after_frame, text="After", font=("Arial", 12, "bold"))
        label_after.pack()
        # Add your after image display widget here

        # Reconstruction Image Frame
        reconstruction_frame = ttk.Frame(images_row_frame)
        reconstruction_frame.grid(row=0, column=2, padx=10)
        label_reconstruction = tk.Label(
            reconstruction_frame, text="Reconstruction", font=("Arial", 12, "bold")
        )
        label_reconstruction.pack()
        # Add your reconstruction image display widget here


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

    # def display_image(self, image, frame_num):
    #     image = image.resize((200, 200), Image.ANTIALIAS)
    #     photo = ImageTk.PhotoImage(image)
    #     label = ttk.Label(self.right_side_bar.grid_slaves()[0], image=photo)
    #     label.image = photo
    #     label.grid(row=0, column=frame_num)

    # Trong hàm run_pca
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
