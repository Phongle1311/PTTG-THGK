import os
import numpy as np

import cv2 as cv

from PIL import Image
import matplotlib.image as mpimg


def load_and_preprocess_dataset(IMG_DIR):
    images = []
    images_flatten = []
    max_images = 200

    total = sum(1 for entry in os.scandir(IMG_DIR) if entry.is_file())
    count = 1
    if total < max_images:
        max_images = total
    for img_path in os.listdir(IMG_DIR):
        if count == max_images + 1:
            break
        img_array = cv.imread(os.path.join(IMG_DIR, img_path), cv.IMREAD_GRAYSCALE)
        img_pil = Image.fromarray(img_array)
        img_64 = np.array(img_pil.resize((64, 64), Image.ANTIALIAS))
        images.append(img_64)
        img_array = img_64.flatten()
        images_flatten.append(img_array)
        count += 1

    images_flatten = np.asarray(images_flatten).T

    return images, images_flatten


def mse(predict, actual):
    return np.square(predict - actual).sum(axis=1).mean()


def get_variance_explained(evals):
    """
    Plots eigenvalues.

    Args:
    (numpy array of floats) : Vector of eigenvalues

    Returns:
    Nothing.

    """

    # Cumulatively sum the eigenvalues
    csum = np.cumsum(evals)

    # Normalize by the sum of eigenvalues
    variance_explained = csum / np.sum(evals)

    return variance_explained

    # Calculate the variance explained
    # variance_explained = get_variance_explained(evals)

    # Visualize
    # with plt.xkcd():
    # plot_variance_explained(variance_explained)


def save_images(reconstructed_img):
    output_folder = "reconstructed_images"
    os.makedirs(output_folder, exist_ok=True)

    total = reconstructed_img.shape[1]
    for i in range(total):
        image = reconstructed_img[:, i].reshape((64, 64))
        # Hiển thị hình ảnh sử dụng Matplotlib
        output_path = f"reconstructed_images/reconstructed_image_{i}.png"  # Điều chỉnh đường dẫn và tên tệp
        mpimg.imsave(output_path, image)
