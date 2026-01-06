

import os
import skimage
import matplotlib.pyplot as plt

from skimage import io, color
from skimage.transform import resize
from skimage.io import imsave
import numpy as np


# First operation: RGB --> Grayscale


image_directory = r'\Users\ardal\Downloads\472\Sample\Old'

files = os.listdir(image_directory)

for file in files:

    file_path = os.path.join(image_directory, file)

    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        
        image = io.imread(file_path)

        grayscale_image = color.rgb2gray(image)

        gray_image_path = os.path.join(image_directory, os.path.splitext(file)[0] + '_gray.jpg')

        imsave(gray_image_path, grayscale_image)

print("Processing complete!")


# Second operation: resize the grayscaled photo to 100 x 100 resolution


def resize_img(image_path, output_path, target_size):

    image = io.imread(image_path)
    aspect_ratio = image.shape[1] / image.shape[0]

    if target_size[0] / aspect_ratio <= target_size[1]:
    
        new_width = target_size[0]
        new_height = int(target_size[0] / aspect_ratio)
        
    else:
        new_height = target_size[1]
        new_width = int(target_size[1] * aspect_ratio)

    resized_image = resize(image, (new_height, new_width), anti_aliasing=True)
    io.imsave(output_path, (resized_image * 255).astype(np.uint8))


def resize_images(input_folder, output_folder, target_size):

    if not os.path.exists(output_folder):
    
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
    
        if filename.lower().endswith(('gray.png', 'gray.jpg', 'gray.jpeg', 'gray.tiff', 'gray.bmp', 'gray.gif')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            resize_img(input_path, output_path, target_size)


if __name__ == "__main__":

    input_folder = r'C:\Users\ardal\Downloads\472\Sample\Old'
    output_folder = r'C:\Users\ardal\Downloads\472\Sample\New'
    
    target_size = (100, 100)

    resize_images(input_folder, output_folder, target_size)
