import os
import numpy as np

import cv2 as cv

from PIL import Image


def load_and_preprocess_dataset(IMG_DIR):
    images = []
    images_flatten = []

    total = sum(1 for entry in os.scandir(IMG_DIR) if entry.is_file())
    count = 1
    max_images = min(total, 200)
    for img_path in os.listdir(IMG_DIR):
        if count == max_images + 1:
            break
        img_array = cv.imread(os.path.join(IMG_DIR, img_path), cv.IMREAD_GRAYSCALE)
        img_pil = Image.fromarray(img_array)
        img_64 = np.array(img_pil.resize((64, 64), Image.ANTIALIAS))
        images.append(img_64)
        images_flatten.append(img_64.flatten())
        count += 1

    images_flatten = np.asarray(images_flatten)

    return images, images_flatten
