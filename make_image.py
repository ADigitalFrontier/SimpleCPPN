"""
Function for making an image from a CPPN

Author:     Aaron Stone
Date:       09/01/2022
"""
from PIL import Image
import os


def run_cppn(cppn, in_args):
    out_coords = []
    for coordinates in in_args:
        cppn.set_inputs(coordinates)
        out_coords.append(cppn.evaluate())
        
    return out_coords


def make_image(cppn, IMAGE_X, IMAGE_Y, image_directory=None, save=True, resize_x=256, resize_y=256):
    image = Image.new("RGB", (IMAGE_X, IMAGE_Y))

    for y in range(IMAGE_Y):
        for x in range(IMAGE_X):
            cppn.set_inputs([x/IMAGE_X, y/IMAGE_Y])
            out = cppn.evaluate()

            r = int(abs(out[0])*255)
            g = int(abs(out[1])*255)
            b = int(abs(out[2])*255)

            image.putpixel((x, y), (r, g, b))

    image = image.resize((resize_x, resize_y), Image.ANTIALIAS)

    if image_directory is not None:
        images_count = len(os.listdir(image_directory))
        if save:
            image.save(image_directory + str(images_count) + "image.png")

    return image


def make_image_with_output_coords(cppn, IMAGE_X, IMAGE_Y, image_directory=None, save=True, resize_x=256, resize_y=256):
    image = Image.new("RGB", (IMAGE_X, IMAGE_Y))

    for y in range(IMAGE_Y):
        for x in range(IMAGE_X):
            cppn.set_inputs([x/IMAGE_X, y/IMAGE_Y])
            out = cppn.evaluate()

            r = int(abs(out[0])*255)
            g = int(abs(out[1])*255)
            b = int(abs(out[2])*255)

            x_out = int(abs(out[3]*(IMAGE_X-1)))
            y_out = int(abs(out[4]*(IMAGE_Y-1)))

            image.putpixel((x_out, y_out), (r, g, b))

    image = image.resize((resize_x, resize_y), Image.ANTIALIAS)

    if image_directory is not None:
        images_count = len(os.listdir(image_directory))
        if save:
            image.save(image_directory + str(images_count) + "image.png")

    return image