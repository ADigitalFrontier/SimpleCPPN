"""
Author:     Aaron Stone
Date:       09/01/2022
"""

"""
TODO:
    add activation probability table optional argument
    add evolution probability table argument
"""


import networkx as nx
import matplotlib.pyplot as plt
from Activations import identity_activation, ActivationFunctionSet
import json
import random
import os

DEFAULT_SET = ActivationFunctionSet()

class Component:
    def __init__(self, directory=None):
        if directory is not None:
             with open(directory+"/data.json", 'r') as f:
                data = json.load(f)
                self.inputs = data["inputs"]
                self.hidden = data["hidden"]
                self.outputs = data["outputs"]
                self.graph = nx.read_gpickle(directory+"/component.pkl")
        else:
            self.inputs = []
            self.hidden = []
            self.outputs = []
            self.graph = nx.DiGraph()

        ids = [i for i in self.graph.nodes()]
        if len(ids) == 0:
            self.size = 0
        else:
            self.size = max(ids)


    def save(self, directory):
        data_dict = {"inputs": self.inputs, "hidden": self.hidden, "outputs": self.outputs}
        # create the directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(directory+"/data.json", 'w') as f:
            json.dump(data_dict, f)
        nx.write_gpickle(self.graph, directory+"/component.pkl")


    def show(self):
        labels = nx.get_node_attributes(self.graph, 'label')
        colors = nx.get_node_attributes(self.graph, 'color')
        positions = nx.get_node_attributes(self.graph,'position')
        nx.draw(self.graph, with_labels=True, pos=positions, node_color=colors.values(), labels=labels, font_size=8, arrows=True)
        plt.show()


    def add_node(self, node_type="hidden", position=None, color="black"):
        self.size += 1
        if node_type == "input":
            self.inputs.append(self.size)
        elif node_type == "hidden":
            self.hidden.append(self.size)
        elif node_type == "output":
            self.outputs.append(self.size)
        else:
            raise Exception("Node type not recognized")
        self.graph.add_node(self.size, node_type=node_type)
        # get the node and return it
        node = self.graph.nodes[self.size]
        
        if position is None:
            position = (random.random()*.9+.05, 0-random.random()*.9-.05)

        node['position'] = position
        node['color'] = color
        node['name'] = self.size
        node['value'] = 0
        node['activation'] = identity_activation
        if node_type == "hidden":
            node['age'] = 0
        return node

    
    def evaluate(self):
        # for all non-input nodes, set the value to 0
        for node in self.graph.nodes():
            if node not in self.inputs:
                self.graph.nodes[node]['value'] = 0

        # topological sort the graph
        sorted_nodes = nx.topological_sort(self.graph)
        for node in sorted_nodes:
            # get all outgoing connections
            outgoing_edges = self.graph.out_edges(node)
            for edge in outgoing_edges:
                try:
                    # get terminal node
                    terminal_node = self.graph.nodes[edge[1]]
                    # get the weight of the edge
                    weight = self.graph.edges[edge]['weight']
                    # get the value of the root node
                    root_node = self.graph.nodes[node]
                    # if the root node has an activation function, apply it
                    root_value = root_node['value']
                    root_value = root_node['activation'](root_value)
                    terminal_node['value'] += root_value * weight
                except Exception as e:
                    # print("Error [113]: ", e, edge, node)
                    pass
        
        # clamp the values to be between 0 and 1
        outputs = []
        for node in self.outputs:
            out = max(0, min(1, self.graph.nodes[node]['value']))
            outputs.append(out)
        return outputs

    def evolve(self, add_node_amount=None, add_edge_amount=None, edge_mutate_rate=.1, node_mutate_rate=.1, prob_table=None):
        STABILIZATION_AGE = 100

        # add one to the age of all hidden nodes
        for node in self.hidden:
            try:
                self.graph.nodes[node]['age'] += 1
            except Exception as e:
                pass 
                # print("Error: ", e, node)
        # add one to the age of all edges
        for edge in self.graph.edges:
            try:
                self.graph.edges[edge]['age'] += 1
            except Exception as e:
                pass
                # print("Error: ", e, edge)

        if prob_table is None:
            PROB_TABLE = {
                "edge": {
                    "remove": 0.1,
                    "change": .9
                },
                "node": {
                    "neutralize": .3,
                    "remove": 0.3,
                    "change": .4
                },
                "intercept_rate": .6,
            }
        else:
            PROB_TABLE = prob_table

        def get_edge_modification(edge):
            amount = random.random()*2-1
            modification = 1-(edge['age']/STABILIZATION_AGE)
            return amount*modification


        def get_prob(object):
            return (1-(object['age']/STABILIZATION_AGE))


        # pick a random integer from -5 to 5
        if add_node_amount is None:
            add_node_amount = max(0, random.randint(-5, 5))

        for i in range(add_node_amount):
            if random.random() < PROB_TABLE["intercept_rate"]:
                # find an edge
                edge = random.choice(list(self.graph.edges()))
                # get the edge's weight
                weight = self.graph.edges[edge]['weight']
                # get the edge's age
                age = self.graph.edges[edge]['age']
                # disconnect the edge
                self.graph.remove_edge(edge[0], edge[1])
                # add a new node
                new_node = self.add_node(node_type="hidden")
                # add the edge back
                self.graph.add_edge(edge[0], new_node['name'], weight=weight)
                self.graph.add_edge(new_node['name'], edge[1], weight=weight)
                # get the edge
                edge1 = self.graph.edges[edge[0], new_node['name']]
                edge2 = self.graph.edges[new_node['name'], edge[1]]
                # set the age of the edge
                edge1['age'] = age
                edge2['age'] = age
            else:
                self.add_node(node_type="hidden")


        # pick a random integer from -5 to 5
        if add_edge_amount is None:
            add_edge_amount = max(0, random.randint(-5, 5))
        
        for i in range(add_edge_amount):
            # pick two nodes
            node_pool_1 = [self.inputs, self.hidden]
            node_pool_2 = [self.hidden, self.outputs]
            node1 = random.choice(node_pool_1)
            node2 = random.choice(node_pool_2)
            # if the nodes are the same, pick another one
            while node1 == node2:
                node1 = random.choice(node_pool_1)
                node2 = random.choice(node_pool_2)
            # add the edge
            self.graph.add_edge(node1[0], node2[0], weight=random.random()*2-1, age=0)

        # for each hidden node
        for node in list(self.hidden):
            try:
                if random.random() < node_mutate_rate * get_prob(self.graph.nodes[node]):
                    rand_num = random.random()
                    neutralize_threshold = PROB_TABLE["node"]["neutralize"]
                    remove_threshold = neutralize_threshold+PROB_TABLE["node"]["remove"]
                    change_threshold = remove_threshold+PROB_TABLE["node"]["change"]
                    if rand_num < neutralize_threshold:
                        # neutralize the node
                        self.graph.nodes[node]['activation'] = identity_activation
                    elif rand_num < remove_threshold:
                        # remove the node
                        self.graph.remove_node(node)
                    elif rand_num < change_threshold:
                        # change the node's activation
                        self.graph.nodes[node]['activation'] = DEFAULT_SET.get_random()
            except Exception as e:
                # print("Error [222]: ", e, node)
                pass

        # for each edge
        for edge in list(self.graph.edges):
            try:
                if random.random() < edge_mutate_rate * get_prob(self.graph.edges[edge]):
                    rand_num = random.random()
                    remove_threshold = PROB_TABLE["edge"]["remove"]
                    change_threshold = remove_threshold+PROB_TABLE["edge"]["change"]
                    if rand_num < remove_threshold:
                        # remove the edge
                        self.graph.remove_edge(edge[0], edge[1])
                    elif rand_num < change_threshold:
                        # change the edge's weight
                        self.graph.edges[edge]['weight'] += get_edge_modification(self.graph.edges[edge])
            except Exception as e:
                # print("Error [238]: ", e, edge)
                pass