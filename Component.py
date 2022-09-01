import networkx as nx
import matplotlib.pyplot as plt
from Activations import identity_activation
import random
import json
import os

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


    def add_node(self, node_type="hidden", position=(0, 0), color="black"):
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
        node['position'] = position
        node['color'] = color
        node['name'] = self.size
        node['value'] = 0
        node['activation'] = identity_activation
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
        
        return [self.graph.nodes[node]['value'] for node in self.outputs]




"""
comp1 = Component()
node = comp1.add_node("input")
node["coordinates"] = [0,5,1,3,8]
comp1.save("comp1")
"""