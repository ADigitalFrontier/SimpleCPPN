"""
Test for generating random CPPNs.

Author:     Aaron Stone
Date:       09/01/2022
"""
from make_cppn import make_cppn
from PIL import Image
import os


IMAGE_X = 32
IMAGE_Y = 32
NUMBER_ITERATIONS = 100
SHOW_CPPN = False
PAUSE_BETWEEN = False


directory = "images/"

# create the directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

for i in range(NUMBER_ITERATIONS):
    cppn = make_cppn(num_inputs=2, num_outputs=3, num_hnodes=10, num_connections=10)
    if SHOW_CPPN:
        cppn.show()
    if PAUSE_BETWEEN:
        # wait for input
        input("Press Enter to continue...")
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
    images_count = len(os.listdir(directory))
    # get size of cppns/ directory
    cppns_count = len(os.listdir("cppns"))
    # save image to images/ directory
    image.save(directory + str(images_count) + ".png")
    image.show()
    cppn.save("cppns/"+str(cppns_count))