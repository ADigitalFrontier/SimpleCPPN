"""
Test for generating random CPPNs.

Author:     Aaron Stone
Date:       09/01/2022
"""
from make_cppn import make_cppn
from make_image import make_image
import networkx as nx
import os


# GENERATOR SETTINGS
IMAGE_X = 32
IMAGE_Y = 32
NUMBER_ITERATIONS = 50
SHOW_CPPN = False
PAUSE_BETWEEN = False
DISCARD_DISCONNECTED = True
SHOW_IMAGES = False
EVOLVE = False

# CPPN SETTINGS
NUM_INPUTS = 2
NUM_OUTPUTS = 3
NUM_HIDDEN = 18
NUM_CONNECTIONS = 54

# FILE LOCATION SETTINGS
image_directory = "images/"
cppn_directory = "cppns/"


# create the directory if it doesn't exist
if not os.path.exists(image_directory):
    os.makedirs(image_directory)
if not os.path.exists(cppn_directory):
    os.makedirs(cppn_directory)


for i in range(NUMBER_ITERATIONS):
    cppn = make_cppn(num_inputs=NUM_INPUTS, num_outputs=NUM_OUTPUTS, num_hnodes=NUM_HIDDEN, num_connections=NUM_CONNECTIONS)
    if EVOLVE:
        cppn.evolve()
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

    cppns_count = len(os.listdir(cppn_directory))
    image = make_image(cppn, IMAGE_X, IMAGE_Y, image_directory, save=True)
    if SHOW_IMAGES:
        image.show()
    cppn.save(cppn_directory+str(cppns_count))
