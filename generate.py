"""
Test for generating random CPPNs.

Author:     Aaron Stone
Date:       09/01/2022
"""
from make_cppn import make_cppn
from PIL import Image
import networkx as nx
import os


IMAGE_X = 32
IMAGE_Y = 32
NUMBER_ITERATIONS = 100
SHOW_CPPN = False
PAUSE_BETWEEN = False
DISCARD_DISCONNECTED = True
SHOW_IMAGES = False

NUM_INPUTS = 2
NUM_OUTPUTS = 3
NUM_HIDDEN = 18
NUM_CONNECTIONS = 54


image_directory = "images/"
cppn_directory = "cppns/"

# create the directory if it doesn't exist
if not os.path.exists(image_directory):
    os.makedirs(image_directory)
if not os.path.exists(cppn_directory):
    os.makedirs(cppn_directory)

for i in range(NUMBER_ITERATIONS):
    cppn = make_cppn(num_inputs=NUM_INPUTS, num_outputs=NUM_OUTPUTS, num_hnodes=NUM_HIDDEN, num_connections=NUM_CONNECTIONS)
    if SHOW_CPPN:
        cppn.show()
    if PAUSE_BETWEEN:
        # wait for input
        input("Press Enter to continue...")

    if DISCARD_DISCONNECTED:
        # if there isn't a path from at least one input to at least one output, discard the CPPN
        valid = False
        for inode in cppn.inputs:
            for onode in cppn.outputs:
                if nx.has_path(cppn.graph, inode, onode):
                    valid = True
                    break
        if not valid:
            print("Skipping disconnected CPPN")
            continue


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
    images_count = len(os.listdir(image_directory))
    # get size of cppns/ directory
    cppns_count = len(os.listdir(cppn_directory))
    # save image to images/ directory
    image.save(image_directory + str(images_count) + ".png")
    if SHOW_IMAGES:
        image.show()
    cppn.save(cppn_directory+str(cppns_count))