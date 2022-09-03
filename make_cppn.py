"""
Function for making a CPPN

Author:     Aaron Stone
Date:       09/01/2022
"""

from Component import Component
from Activations import ActivationFunctionSet
import random

DEFAULT_SET = ActivationFunctionSet()

def make_cppn(num_inputs=2, num_outputs=1, num_hnodes=10, num_connections=10):
    cppn = Component()

    inputs = []
    hnodes = []
    outputs = []

    node_count = 1

    for i in range(num_inputs):
        inode = cppn.add_node(node_type="input", position=(i/num_inputs, 0), color="blue")
        inode['label'] = "Input_" + str(i)
        inputs.append(node_count)
        node_count += 1

    for _ in range(1, num_hnodes):
        hnode = cppn.add_node(node_type="hidden", position=(random.random()*.9+.05, 0-random.random()*.9-.05), color="yellow")
        activation = DEFAULT_SET.get_random()
        hnode['activation'] = activation
        hnode['label'] = activation.__name__
        hnodes.append(node_count)
        node_count += 1

    for i in range(num_outputs):
        onode = cppn.add_node(node_type="output", position=(i/num_outputs, -1), color="green")
        onode['label'] = "Output_" + str(i)
        outputs.append(node_count)
        node_count += 1

    node_pool_a = inputs + hnodes
    node_pool_b = hnodes + outputs
    for i in range(num_connections):
        invalid = True
        while invalid:
            node_a = random.choice(node_pool_a)
            node_b = random.choice(node_pool_b)
            if node_a < node_b:
                invalid = False
        cppn.graph.add_edge(node_a, node_b, weight=random.random()*2-1, age=0)
        # get the edge
        edge = cppn.graph[node_a][node_b]

    return cppn


def load_cppn(directory):
    cppn = Component(directory)
    return cppn