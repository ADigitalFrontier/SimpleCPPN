"""
Test for generating random CPPNs.

Author:     Aaron Stone
Date:       09/01/2022
"""
from make_cppn import load_cppn, make_cppn
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from make_image import make_image
from PIL import ImageFont
from PIL import ImageDraw
import os


ORIGINAL = None # "evolutions/iteration_0/5"
SAVE_DIR = "evolutions"
IMAGE_X = 16
IMAGE_Y = 16
NUM_PER_GENERATION = 100

# create the directory if it doesn't exist
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# CPPN SETTINGS
NUM_INPUTS = 2
NUM_OUTPUTS = 3
NUM_HIDDEN = 17
NUM_CONNECTIONS = 36
LABEL_FONT = 72

PROB_TABLE = {
    "edge": {
        "remove": 0.1,
        "change": .9
    },
    "node": {
        "neutralize": .2,
        "remove": 0.3,
        "change": .5
    },
    "intercept_rate": .6,
}

current_path = ""
keep_going = True

current_dir = SAVE_DIR
current_cppn = ORIGINAL

# get the number of files in the current directory
num_iterations = 0
for item in os.listdir(current_dir):
    # if name starts with "iteration_"
    if item.startswith("iteration_"):
        num_iterations += 1

# create a new directory for the iteration
current_dir = current_dir + "/" + "iteration_"+str(num_iterations)
os.mkdir(current_dir)

while keep_going:
    images = []
    for i in range(NUM_PER_GENERATION):
        if ORIGINAL is not None or current_cppn is not None:
            cppn = load_cppn(current_cppn)
            cppn.evolve(add_node_amount=5, add_edge_amount=5, edge_mutate_rate=.15, node_mutate_rate=.15, prob_table=PROB_TABLE)
        else:
            cppn = make_cppn(num_inputs=NUM_INPUTS, num_outputs=NUM_OUTPUTS, num_hnodes=NUM_HIDDEN, num_connections=NUM_CONNECTIONS)
        cppn_dir = current_dir + "/" + str(i)
        cppn.save(cppn_dir)
        images.append(make_image(cppn, IMAGE_X, IMAGE_Y, image_directory=current_dir, save=False, resize_x=256, resize_y=256))
    
    # create a row of images from array images
    image_row = Image.new("RGB", (256 * NUM_PER_GENERATION, 256+LABEL_FONT))
    for i in range(NUM_PER_GENERATION):
        # add a number label to the image
        draw = ImageDraw.Draw(image_row)
        # use 48pt font
        font = ImageFont.truetype("arial.ttf", LABEL_FONT)
        # use 48pt font
        draw.text((i*256, 0),str(i),(255,255,255), font=font)
        image_row.paste(images[i], (i * 256, LABEL_FONT))
        
    # save image row to current_dir
    image_row.save(current_dir + "/image_row.png")
    # show image row
    image_row.show()

    # ask user to select a descendant
    chosen_descendant = input("Which lineage to continue? (0-" + str(NUM_PER_GENERATION-1) + ") ")
    if chosen_descendant == "" or chosen_descendant.lower() == "q":
        keep_going = False
    else:
        current_cppn = current_dir + "/" + str(chosen_descendant)
        current_dir = current_dir + "/" + "lineage_"+str(chosen_descendant)
        if not os.path.exists(current_dir):
            os.makedirs(current_dir)
