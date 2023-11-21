import os
import numpy as np
from matplotlib.image import imread
import matplotlib.pyplot as plt
from tkinter import Tk, Button, filedialog, Scale
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def img2double(img):
    info = np.iinfo(img.dtype)
    return img.astype(float) / info.max

def svd(img, full_matrices=False):
    U, S, VT = np.linalg.svd(img, full_matrices=full_matrices)
    return U, np.diag(S), VT

def update_compressed_image(value):
    global RANK
    RANK = int(value)

def release_update_compressed_image(value):
    global RANK
    RANK = int(value)

    red_channel, green_channel, blue_channel = img[:, :, 0], img[:, :, 1], img[:, :, 2]

    U_B, S_B, VT_B = svd(blue_channel)
    U_G, S_G, VT_G = svd(green_channel)
    U_R, S_R, VT_R = svd(red_channel)

    XR_r = U_R[:, :RANK] @ S_R[:RANK, :RANK] @ VT_R[:RANK, :]
    XG_r = U_G[:, :RANK] @ S_G[:RANK, :RANK] @ VT_G[:RANK, :]
    XB_r = U_B[:, :RANK] @ S_B[:RANK, :RANK] @ VT_B[:RANK, :]

    X_r = np.dstack((XR_r, XG_r, XB_r))

    # Update the compressed image canvas
    ax_compressed.clear()
    ax_compressed.imshow(X_r)
    ax_compressed.set_title(f'Compressed Image (Rank {RANK})')
    canvas_compressed.draw()

def add_image():
    global img, canvas_original, canvas_compressed, slider

    file_path = filedialog.askopenfilename()
    if file_path:
        img = imread(file_path)
        img = img2double(img)

        # Update the original image canvas
        ax_original.clear()
        ax_original.imshow(img)
        ax_original.set_title('Original Image')
        canvas_original.draw()

        # Update the compressed image canvas
        update_compressed_image(RANK)

def on_closing():
    root.destroy()

# Default rank value
RANK = 5

# Create the Tkinter window
root = Tk()
root.title('Image Compression using SVD')

# Create a button to add an image
add_button = Button(root, text='Add Image', command=add_image)
add_button.pack()

# Create a slider for adjusting the rank
slider = Scale(root, from_=1, to=100, orient='horizontal', label='Rank', command=update_compressed_image, resolution=1, length=300)
slider.set(RANK)
slider.pack()

# Create a figure for the original image on the left
fig_original = plt.Figure(figsize=(6, 6))
ax_original = fig_original.add_subplot(111)
canvas_original = FigureCanvasTkAgg(fig_original, master=root)
canvas_original.get_tk_widget().pack(side='left')

# Create a figure for the compressed image on the right
fig_compressed = plt.Figure(figsize=(6, 6))
ax_compressed = fig_compressed.add_subplot(111)
canvas_compressed = FigureCanvasTkAgg(fig_compressed, master=root)
canvas_compressed.get_tk_widget().pack(side='right')

# Set up the release event for the slider
slider.bind("<ButtonRelease-1>", lambda event: release_update_compressed_image(slider.get()))

# Set up the window closing event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the Tkinter main loop
root.mainloop()
