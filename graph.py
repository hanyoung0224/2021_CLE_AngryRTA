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
    def __init__(self, inNode: Node, outNode: Node):
        self.inNode = inNode
        self.outNode = outNode
        self.distance = sqrt(
            (inNode.location[0] - outNode.location[0]) ** 2
            + (inNode.location[1] - outNode.location[1]) ** 2
        )


class Intersect:
    def __init__(self, node: Node):
        self.name = node.name
        self.neighborhoods = node.neighborhoods
        self.traf_signals = {}
        self._init_signals()

    def _init_signals(self):
        for N1 in self.neighborhoods:
            for N2 in self.neighborhoods:
                if N1 != N2:
                    self.traf_signals[(N1, N2)] = (
                        1,  # green light duration (s)
                        0,  # red light duration (s)
                        0   # standard time (s)
                    )


class Graph:
    def __init__(self):  # std_speed (km/h)
        self.nodes = {}
        self.intersects = {}
        self.time = 0                # (s)
        self.std_speed = 20.3987686  # (m/s)
        self.mileage = \
            lambda x: 2285.93762 + 132.7298916 * x - \
            0.251032407 * (x ** 2)  # input: (m/s), output: (m/L)
        self.std_mileage = self.mileage(self.std_speed)
        self.mass = 1510  # (kg)
        self.efficiency = 0.38
        self.energy_per_liter = 32.6e6  # (J/L)
        self.oiluse = \
            lambda x: (x ** 2) * self.mass / 2 / \
            self.efficiency / self.energy_per_liter  # input: (m/s), output: (L)
        self.std_oiluse = self.oiluse(self.std_speed)

    def add_node(self, name: str, location: tuple):
        node = Node(name, location)
        self.nodes[node.name] = node

    def add_edge(self, inNode_name: str, outNode_name: str):
        inNode = self.nodes[inNode_name]
        outNode = self.nodes[outNode_name]
        edge = Edge(inNode, outNode)
        inNode.edges.append(edge)
        if outNode_name not in inNode.neighborhoods:
            inNode.neighborhoods.append(outNode_name)
        if inNode_name not in outNode.neighborhoods:
            outNode.neighborhoods.append(inNode_name)

    def init_intersects(self):
        for node in self.nodes.values():
            if len(node.neighborhoods) >= 2:
                self.intersects[node.name] = Intersect(node)

    def set_signal(
            self,
            intersect_name: str,
            N1_name: str,
            N2_name: str,
            signal: tuple
    ):
        intersect = self.intersects[intersect_name]
        intersect.traf_signals[(N1_name, N2_name)] = signal

    def distance(self, inNode_name: str, outNode_name: str):
        inNode = self.nodes[inNode_name]
        outNode = self.nodes[outNode_name]
        return sqrt(
            (inNode.location[0] - outNode.location[0]) ** 2
            + (inNode.location[1] - outNode.location[1]) ** 2
        )

    def find_route(self, startNode_name: str, endNode_name: str):
        open_queue, close_queue = [], {}
        selected = (
            self.std_oiluse,  # F = G + H
            self.std_oiluse,  # G: total cost so far
            0,                # H: heuristic cost
            startNode_name,   # current node name
            None,             # parent node name
            0                 # T: required time (s)
        )
        while selected[3] != endNode_name:
            close_queue[selected[3]] = selected
            selectedNode = self.nodes[selected[3]]
            for edge in selectedNode.edges:
                intersect = self.intersects.get(selected[3], None)
                time_now = selected[5] + self.time
                isClosed = close_queue.get(edge.outNode.name, False)
                if not isClosed:
                    if intersect and selected[4]:
                        signal = intersect.traf_signals[(selected[4], edge.outNode.name)]
                        if signal[0] == 0:
                            continue
                        time_in_cycle = (time_now - signal[2]) % (signal[0] + signal[1])
                        if time_in_cycle <= signal[0]:
                            G = selected[1] + edge.distance / self.std_mileage
                            T = selected[5] + edge.distance / self.std_speed
                        else:
                            selected_past = close_queue[selected[4]]
                            distance_past = self.distance(selected[4], selected[3])
                            time_past = selected_past[5] + self.time
                            time_fast = (2 * signal[0] + signal[1]) - \
                                (time_past - signal[2]) % (signal[0] + signal[1])
                            fast_speed = distance_past / time_fast
                            fast_mileage = self.mileage(fast_speed)
                            fast_oiluse = self.oiluse(fast_speed) - self.std_oiluse
                            G_fast = selected_past[1] + distance_past / fast_mileage + \
                                fast_oiluse + edge.distance / self.std_mileage
                            T_fast = selected_past[5] + distance_past / fast_speed + \
                                edge.distance / self.std_speed
                            time_slow = 2 * (signal[0] + signal[1]) - \
                                (time_past - signal[2]) % (signal[0] + signal[1])
                            slow_speed = distance_past / time_slow
                            slow_mileage = self.mileage(slow_speed)
                            slow_oiluse = self.std_oiluse - self.oiluse(slow_speed)
                            G_slow = selected_past[1] + distance_past / slow_mileage + \
                                slow_oiluse + edge.distance / self.std_mileage
                            T_slow = selected_past[5] + distance_past / slow_speed + \
                                edge.distance / self.std_speed
                            G_stop = selected[1] + edge.distance / self.std_mileage + \
                                self.std_oiluse
                            T_stop = selected[5] + (signal[0] + signal[1] - time_in_cycle) + \
                                edge.distance / self.std_speed
                            G, T = list(sorted([
                                (G_fast, T_fast),
                                (G_slow, T_slow),
                                (G_stop, T_stop)
                            ]))[0]
                    else:
                        G = selected[1] + edge.distance / self.std_mileage
                        T = selected[5] + edge.distance / self.std_speed
                    H = self.distance(edge.outNode.name, endNode_name) / self.std_mileage
                    F = G + H
                    heappush(open_queue, (F, G, H, edge.outNode.name, edge.inNode.name, T))
            selected = heappop(open_queue)
        oiluse = selected[1]
        route = [selected[3]]
        required_time = selected[5]
        while selected[4]:
            route.append(selected[4])
            selected = close_queue[selected[4]]
        route = list(reversed(route))
        return route, oiluse, required_time

    def _render_graph(self):
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
            plt.axis('off')

    def show(self, figsize=(8, 8)):
        plt.figure(figsize=figsize)
        self._render_graph()
        plt.show()

    def _render_route(self, startNode_name: str, endNode_name: str):
        self._render_graph()
        route, oiluse, required_time = \
            self.find_route(startNode_name, endNode_name)
        x, y = [], []
        for node_name in route:
            node = self.nodes[node_name]
            x.append(node.location[0])
            y.append(node.location[1])
        plt.plot(x, y, c='blue', linewidth=3, zorder=1)
        plt.text(
            -980, 1020, 'Fuel Usage: {}L'.format(round(oiluse, 4)),
            horizontalalignment='left',
            verticalalignment='top',
            size=16,
            weight='bold',
            zorder=10
        )
        plt.text(
            -980, 970, 'Required Time: {}s'.format(round(required_time, 4)),
            horizontalalignment='left',
            verticalalignment='top',
            size=16,
            weight='bold',
            zorder=10
        )

    def show_route(
            self,
            startNode_name: str,
            endNode_name: str,
            figsize=(8, 8)
    ):
        plt.figure(figsize=figsize)
        self._render_route(startNode_name, endNode_name)
        plt.show()

    def save_route(
            self,
            startNode_name: str,
            endNode_name: str,
            filepath: str,
            figsize=(8, 8)
    ):
        plt.figure(figsize=figsize)
        self._render_route(startNode_name, endNode_name)
        plt.savefig(filepath)
