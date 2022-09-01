from Component import Component
from Activations import ActivationFunctionSet
from PIL import Image
import networkx as nx
import random
import os
import math

DEFAULT_SET = ActivationFunctionSet()

def make_cppn(min_hnodes, max_hnodes, min_connections, max_connections):
    cppn = Component()

    x = cppn.add_node(node_type="input", position=(0, 0), color="blue")
    x['label'] = "X"
    y = cppn.add_node(node_type="input", position=(1, 0), color="red")
    y['label'] = "Y"

    hnodes = []
    num_hidden = random.randint(min_hnodes, max_hnodes)
    for _ in range(1, num_hidden):
        hnode = cppn.add_node(node_type="hidden", position=(random.random()*.9+.05, 0-random.random()*.9-.05), color="yellow")
        hnodes.append(hnode)
        activation = DEFAULT_SET.get_random()
        hnode['activation'] = activation
        hnode['label'] = activation.__name__

    r = cppn.add_node(node_type="output", position=(0, -1), color="green")
    r['label'] = "R"
    g = cppn.add_node(node_type="output", position=(.5, -1), color="green")
    g['label'] = "G"
    b = cppn.add_node(node_type="output", position=(1, -1), color="green")
    b['label'] = "B"

    inputs = [x, y]
    outputs = [r,g,b]

    node_pool_a = inputs + hnodes
    node_pool_b = hnodes + outputs
    num_connections = random.randint(min_connections, max_connections)
    for i in range(num_connections):
        invalid = True
        while invalid:
            node_a = random.choice(node_pool_a)['name']
            node_b = random.choice(node_pool_b)['name']
            if node_a < node_b:
                invalid = False
        cppn.graph.add_edge(node_a, node_b, weight=random.random()*2-1)

    return cppn


for cppn_iter in range(50):
    cppn = make_cppn(3, 15, 3, 15)
    # if there is no path from any of the inputs to any of the outputs, skip this cppn
    is_valid = False
    for inode in cppn.inputs:
        for onode in cppn.outputs:
            if nx.has_path(cppn.graph, inode, onode):
                is_valid = True
                break

    if not is_valid:
        print("Invalid cppn, skipping")
        continue

    num_x = 75
    num_y = 75

    # generate image of size num_x x num_y
    image = Image.new("RGB", (num_x, num_y))

    for i in range(num_y):
        y = i/num_x
        row = []
        for j in range(num_x):
            x = j/num_y
            # print("X: " + str(x), "Y: " + str(y))
            cppn.graph.nodes[1]['value'] = x
            cppn.graph.nodes[2]['value'] = y
            out = cppn.evaluate()
            red = int(abs(out[0]) * 255)
            green = int(abs(out[1]) * 255)
            blue = int(abs(out[2]) * 255)
            # set the pixel to the color
            image.putpixel((j, i), (red, green, blue))

    cppn.save("cppns/"+str(cppn_iter))
    # save the imagine in directory called name
    image.save("cppns/"+str(cppn_iter)+"/image.png")


images = []
# for each directory in cppns/, get the image and show it
for subdir in os.listdir("cppns/"):
    # open the image
    images.append(Image.open("cppns/"+subdir+"/image.png"))


row_size = 5
# create a grid from the images
grid = Image.new("RGB", (num_x*len(images), num_y*math.ceil(len(images)/row_size)))

j = -1
for i in range(len(images)):
    if i % row_size == 0:
        j += 1
    print(i, j)
    grid.paste(images[i], (i*num_x, j*num_x))

# save the grid
grid.save("cppns/grid"+str(cppn_iter)+".png")
# show the grid
grid.show()