from Component import Component
from Activations import ActivationFunctionSet
import networkx as nx
import random

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

    brightness = cppn.add_node(node_type="output", position=(0.5, -1), color="green")
    brightness['label'] = "Brightness"

    inputs = [x, y]
    outputs = [brightness]

    node_pool_a = inputs + hnodes
    node_pool_b = hnodes + outputs
    num_connections = random.randint(min_connections, max_connections)
    for i in range(num_connections):
        invalid = True
        while invalid:
            node_a = random.choice(node_pool_a)['name']
            node_b = random.choice(node_pool_b)['name']
            print(node_a, node_b)
            if node_a < node_b:
                invalid = False
        cppn.graph.add_edge(node_a, node_b, weight=random.random()*2-1)

    return cppn


for i in range(10):
    cppn = make_cppn(3, 10, 3, 10)
    cppn.show()
    cppn.save("cppn_"+str(i))