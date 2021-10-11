from math import sqrt
from heapq import heappush, heappop
import matplotlib.pyplot as plt


class Node:
    def __init__(self, name: str, location: tuple):
        self.name = name
        self.location = location
        self.edges = []
        self.neighborhoods = []


class Edge:
    def __init__(self, inNode, outNode):
        self.inNode = inNode
        self.outNode = outNode
        self.distance = sqrt(
            (inNode.location[0] - outNode.location[0]) ** 2
            + (inNode.location[1] - outNode.location[1]) ** 2
        )


class Intersect:
    def __init__(self, node):
        self.name = node.name
        self.neighborhoods = node.neighborhoods
        self.traf_signals = {}

    def update_signals(self):
        for N1 in self.neighborhoods:
            for N2 in self.neighborhoods:
                if N1 != N2:
                    self.traf_signals[(N1, N2)] = self.traf_signals.get((N1, N2), (
                            0,  # green light duration (s)
                            0,  # red light duration (s)
                            0   # standard time (s)
                        )
                    )


class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name: str, location: tuple):
        node = Node(name, location)
        self.nodes[node.name] = node

    def add_edge(self, inNode_name, outNode_name):
        inNode = self.nodes[inNode_name]
        outNode = self.nodes[outNode_name]
        edge = Edge(inNode, outNode)
        inNode.edges.append(edge)
        inNode.neighborhoods.append(outNode_name)
        outNode.neighborhoods.append(inNode_name)

    def distance(self, inNode_name, outNode_name):
        inNode = self.nodes[inNode_name]
        outNode = self.nodes[outNode_name]
        return sqrt(
            (inNode.location[0] - outNode.location[0]) ** 2
            + (inNode.location[1] - outNode.location[1]) ** 2
        )

    def find_route(self, startNode_name, endNode_name):
        open_queue, close_queue = [], {}
        selected = (
            0,  # F = G + H
            0,  # G: total cost so far
            0,  # H: heuristic cost
            startNode_name,  # current node name
            None             # parent node name
        )
        while selected[3] != endNode_name:
            close_queue[selected[3]] = selected
            selectedNode = self.nodes[selected[3]]
            for edge in selectedNode.edges:
                isClosed = close_queue.get(edge.outNode.name, False)
                if not isClosed:
                    G = selected[1] + edge.distance
                    H = self.distance(edge.outNode.name, endNode_name)
                    F = G + H
                    heappush(open_queue, (F, G, H, edge.outNode.name, edge.inNode.name))
            selected = heappop(open_queue)
        route = [selected[3]]
        while selected[4]:
            route.append(selected[4])
            selected = close_queue[selected[4]]
        return list(reversed(route))

    def _build_graph(self):
        edges = []
        for node in self.nodes.values():
            x, y = node.location[0], node.location[1]
            name = node.name
            edges += node.edges
            plt.scatter([x], [y], s=200, c='red', zorder=5)
            plt.text(
                x, y, name,
                horizontalalignment='center',
                verticalalignment='center',
                weight='bold',
                zorder=10
            )
        for edge in edges:
            x = [edge.inNode.location[0], edge.outNode.location[0]]
            y = [edge.inNode.location[1], edge.outNode.location[1]]
            plt.plot(x, y, c='black', zorder=0)

    def show(self, figsize=(8, 8)):
        plt.figure(figsize=figsize)
        self._build_graph()
        plt.axis('off')
        plt.show()

    def show_route(self, startNode_name, endNode_name, figsize=(8, 8)):
        plt.figure(figsize=figsize)
        self._build_graph()
        route = self.find_route(startNode_name, endNode_name)
        x, y = [], []
        for node_name in route:
            node = self.nodes[node_name]
            x.append(node.location[0])
            y.append(node.location[1])
        plt.plot(x, y, c='blue', linewidth=3, zorder=1)
        plt.axis('off')
        plt.show()

