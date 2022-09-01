import networkx as nx
import matplotlib.pyplot as plt
import json

class Component:
    def __init__(self, directory):
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
            self.graph = nx.Graph()

        ids = [i for i in self.graph.nodes()]
        self.size = 0 + max(ids)


    def save(self, directory):
        data_dict = {"inputs": self.inputs, "hidden": self.hidden, "outputs": self.outputs}
        with open(directory+"/data.json", 'w') as f:
            json.dump(data_dict, f)
        nx.write_gpickle(self.graph, directory+"/component.pkl")


    def show(self):
        nx.draw(self.graph, with_labels=True)
        plt.show()


    def add_node(self, node_type="hidden"):
        print("size is ", self.size)
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


comp1 = Component("component")
comp1.show()
comp1.add_node("input")
comp1.show()
comp1.save("component")