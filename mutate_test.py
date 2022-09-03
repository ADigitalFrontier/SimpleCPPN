"""
Test for generating random CPPNs

Author:     Aaron Stone
Date:       09/01/2022
"""
from make_cppn import load_cppn, make_cppn
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from make_image import make_image, make_image_with_output_coords, run_cppn
from PIL import ImageFont
from PIL import ImageDraw
import os


ORIGINAL = None
SAVE_DIR = "evolutions"
IMAGE_X = 24
IMAGE_Y = 24
NUM_PER_GENERATION = 10

# create the directory if it doesn't exist
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# CPPN SETTINGS
NUM_INPUTS = 2
NUM_OUTPUTS = 3
NUM_HIDDEN = 24
NUM_CONNECTIONS = 42
LABEL_FONT = 144
STABILIZATION_AGE = 20
ADD_NODE_AMOUNT = 15
ADD_EDGE_AMOUNT = 15
EDGE_MUTATE_RATE = .125
NODE_MUTATE_RATE = .1

MAP_OUTPUT_COORDS = False
MODIFY_IMAGE = True

TEST_IMAGE = "C:/Users/Aaron/Desktop/test.jpg"

PROB_TABLE = {
    "edge": {
        "remove": .1,
        "change": .7
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


inputs = []
if MODIFY_IMAGE:
    max_dimension = 256
    # scale down the image so the highest dimension is 64
    image = Image.open(TEST_IMAGE)
    # get x and y dimensions
    x_dim = image.size[0]
    y_dim = image.size[1]

    # get highest dimension
    if x_dim > y_dim:
        max_dim = x_dim
        new_x = max_dimension
        new_y = int((y_dim/x_dim) * max_dimension)
    else:
        max_dim = y_dim
        new_y = max_dimension
        new_x = int((x_dim/y_dim) * max_dimension)

    image = image.resize((new_x, new_y), Image.ANTIALIAS)
    # for each pixel in the image, get the RGB values
    for x in range(new_x):
        for y in range(new_y):
            r, g, b = image.getpixel((x, y))
            inputs.append([x/new_x, y/new_y, r, g, b])


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
        if MODIFY_IMAGE:
            cppn = make_cppn(num_inputs=5, num_outputs=3, num_hnodes=NUM_HIDDEN, num_connections=NUM_CONNECTIONS)
        elif ORIGINAL is not None or current_cppn is not None:
            cppn = load_cppn(current_cppn)
            cppn.evolve(add_node_amount=ADD_NODE_AMOUNT, add_edge_amount=ADD_EDGE_AMOUNT, edge_mutate_rate=EDGE_MUTATE_RATE, node_mutate_rate=NODE_MUTATE_RATE, prob_table=PROB_TABLE)
        else:
            if MAP_OUTPUT_COORDS:
                NUM_OUTPUTS += 2
            cppn = make_cppn(num_inputs=NUM_INPUTS, num_outputs=NUM_OUTPUTS, num_hnodes=NUM_HIDDEN, num_connections=NUM_CONNECTIONS)
        cppn_dir = current_dir + "/" + str(i)
        cppn.save(cppn_dir)
        if MODIFY_IMAGE:
            out_coords = run_cppn(cppn, inputs)
            image = Image.new("RGB", (new_x, new_y))
            for index, coord in enumerate(out_coords):
                x = int(abs(inputs[index][0]*new_x))
                y = int(abs(inputs[index][1]*new_y))
                r = int(abs(coord[0] * 255))
                g = int(abs(coord[1] * 255))
                b = int(abs(coord[2] * 255))
                image.putpixel((x, y), (r, g, b))
                # resize the image to the 256x256
            image = image.resize((256, 256), Image.ANTIALIAS)
            images.append(image)
        elif MAP_OUTPUT_COORDS:
            images.append(make_image_with_output_coords(cppn, IMAGE_X, IMAGE_Y, image_directory=current_dir, save=False, resize_x=256, resize_y=256))
        else:
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
