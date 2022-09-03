"""
Test for generating random CPPNs.

Author:     Aaron Stone
Date:       09/01/2022
"""
from PIL import Image
import os


def make_image(cppn, IMAGE_X, IMAGE_Y, image_directory=None, save=True):
    image = Image.new("RGB", (IMAGE_X, IMAGE_Y))
    for y in range(IMAGE_Y):
        for x in range(IMAGE_X):
            cppn.graph.nodes[1]['value'] = x/IMAGE_X
            cppn.graph.nodes[2]['value'] = y/IMAGE_Y
            out = cppn.evaluate()
            red = int(abs(out[0]) * 255)
            green = int(abs(out[1]) * 255)
            blue = int(abs(out[2]) * 255)
            image.putpixel((x, y), (red, green, blue))

    # resize to 256x256
    image = image.resize((256, 256), Image.ANTIALIAS)
    # get size of images/ directory
    if image_directory is not None:
        images_count = len(os.listdir(image_directory))
        if save:
            # save image to images/ directory
            image.save(image_directory + str(images_count) + "image.png")
    return image