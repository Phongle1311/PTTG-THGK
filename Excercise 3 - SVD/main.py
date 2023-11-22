import os
import numpy as np
from matplotlib.image import imread
import matplotlib.pyplot as plt
from tkinter import (
    Label,
    Tk,
    Button,
    filedialog,
    Scale,
    Listbox,
)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Chuyển đổi giá trị của ảnh thành kiểu dữ liệu float trong khoảng từ 0 đến 1.
def img2double(img):
    info = np.iinfo(img.dtype)
    return img.astype(float) / info.max


# Thực hiện phân rã SVD cho một ma trận
def svd(img, full_matrices=False):
    U, S, VT = np.linalg.svd(img, full_matrices=full_matrices)
    return U, np.diag(S), VT


# Cập nhật ảnh nén khi giá trị của thanh trượt thay đổi
def update_compressed_image(value):
    global RANK
    RANK = int(value)


# Cập nhật và hiển thị ảnh nén khi giải phóng sự kiện của thanh trượt
def release_update_compressed_image(value):
    global RANK, img, ax_compressed, canvas_compressed

    RANK = int(value)

    red_channel, green_channel, blue_channel = img[:, :, 0], img[:, :, 1], img[:, :, 2]

    U_B, S_B, VT_B = svd(blue_channel)
    U_G, S_G, VT_G = svd(green_channel)
    U_R, S_R, VT_R = svd(red_channel)

    XR_r = U_R[:, :RANK] @ S_R[:RANK, :RANK] @ VT_R[:RANK, :]
    XG_r = U_G[:, :RANK] @ S_G[:RANK, :RANK] @ VT_G[:RANK, :]
    XB_r = U_B[:, :RANK] @ S_B[:RANK, :RANK] @ VT_B[:RANK, :]

    X_r = np.dstack((XR_r, XG_r, XB_r))

    # Cập nhật canvas hình ảnh nén
    ax_compressed.clear()
    ax_compressed.imshow(X_r)
    ax_compressed.set_title(f"Compressed Image (Rank {RANK})")
    canvas_compressed.draw()
    # Cập nhật và hiển thị kích thước ảnh
    update_image_size(RANK)


# Cho phép người dùng chọn và thêm ảnh mới từ hộp thoại mở tệp
def add_image():
    global img, canvas_original, RANK

    file_path = filedialog.askopenfilename()
    if file_path:
        img = imread(file_path)
        img = img2double(img)

    # Cập nhật canvas hình ảnh nén
    release_update_compressed_image(RANK)

    # Cập nhật và hiển thị kích thước ảnh
    update_image_size(RANK)

# Cập nhật và hiển thị kích thước ảnh khi chọn ảnh mới
def update_image_size(value):
    global img, label_image_size,label_image_pixel,label_image_us,label_image_cs,label_image_cr
    global cs, pixel

    RANK = int(value)

    if img is not None:
        height, width, _ = img.shape
        label_image_size.config(text=f"IMAGE SIZE  {width} x {height} ")
        pixel = width*height
        label_image_pixel.config(text=f"#PIXELS      ={pixel} ")
        label_image_us.config(text=f"UNCOMPRESSED SIZE                   \nproportional to number of pixels")
        cs = width*RANK + RANK + RANK*height
        label_image_cs.config(text=f"COMPRESSED SIZE                     \napproximately proportional to\n{width} x {RANK} + {RANK} + {RANK} x {height}\n={cs}")
        label_image_cr.config(text=f"COMPRESSION RATIO                   \n{pixel} / {cs}\n={pixel/cs}")
# Xử lý sự kiện đóng cửa sổ
def on_closing():
    root.destroy()


# Tạo cửa sổ chính cho ứng dụng
root = Tk()
root.title("Image Compression using SVD")

# Nút này mở hộp thoại mở tệp khi được nhấp để thêm ảnh.
add_button = Button(root, text="Add Image", command=add_image)
add_button.pack()

# Cho phép người dùng chọn giá trị RANK để kiểm soát mức độ nén.
RANK = 5

# Thiết lập thanh slider
slider = Scale(
    root,
    from_=1,
    to=100,
    orient="horizontal",
    label="Rank",
    command=update_compressed_image,
    resolution=1,
    length=300,
)
slider.set(RANK)
slider.pack()

# Label để hiển thị kích thước ảnh
label_image_size = Label(root, text="IMAGE SIZE ")
label_image_size.place(x=100, y=90)
label_image_pixel = Label(root, text="#PIXELS      =")
label_image_pixel.place(x=100, y=110)
label_image_us = Label(root, text="UNCOMPRESSED SIZE ")
label_image_us.place(x=100, y=150)
label_image_cs = Label(root, text="COMPRESSED SIZE ")
label_image_cs.place(x=100, y=190)
label_image_cr = Label(root, text="COMPRESSION RATIO ")
label_image_cr.place(x=100, y=260)


# Hiển thị ảnh nén sau khi áp dụng phương pháp SVD
fig_compressed = plt.Figure(figsize=(4, 4))
ax_compressed = fig_compressed.add_subplot(111)
canvas_compressed = FigureCanvasTkAgg(fig_compressed, master=root)
canvas_compressed.get_tk_widget().pack()


# Thiết lập sự kiện cho thanh slider
slider.bind(
    "<ButtonRelease-1>", lambda event: release_update_compressed_image(slider.get())
)

# Hiển thị tất cả các ảnh gốc trong thư mục 'img' và cho phép người dùng chọn ảnh để xem và nén
listbox = Listbox(root)
listbox.pack(side="bottom")


def create_click_event(canvas, img):
    canvas.mpl_connect("button_press_event", lambda event: on_canvas_click(event, img))


def on_canvas_click(event, template_image):
    print("hehee")
    global img, canvas_original, RANK

    img = template_image

    # Cập nhật canvas hình ảnh nén
    release_update_compressed_image(RANK)
    # Update RANK value here
    update_compressed_image(slider.get())  # Ensure RANK is updated
    release_update_compressed_image(slider.get())

    # Cập nhật và hiển thị kích thước ảnh
    update_image_size(slider.get())


for img_file in os.listdir("img"):
    img_path = os.path.join("img", img_file)
    original_img = imread(img_path)
    original_img = img2double(original_img)

    fig_original = plt.Figure(figsize=(2, 2))
    ax_original = fig_original.add_subplot(111)
    ax_original.imshow(original_img)
    ax_original.axis("off")

    canvas_original = FigureCanvasTkAgg(fig_original, master=listbox)
    canvas_original.get_tk_widget().pack(side="left")

    # Bắt sự kiện click cho mỗi canvas
    create_click_event(canvas_original, original_img)

# Khi người dùng đóng cửa sổ, chương trình sẽ kết thúc
root.protocol("WM_DELETE_WINDOW", on_closing)

# Mở cửa sổ chính
root.mainloop()
