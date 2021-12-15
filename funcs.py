from graph import Graph
import config


def create_graph():
    graph = Graph()
    for i, loc in enumerate(config.node_locations):
        graph.add_node(chr(i + 65), loc)
    for x, y in config.node_edges:
        graph.add_edge(x, y)
        graph.add_edge(y, x)
    for x, y in config.node_edges_onedir:
        graph.add_edge(x, y)
    graph.init_intersects()
    for nodes, signal in config.signals:
        graph.set_signal(nodes[1], nodes[0], nodes[2], signal)
    return graph
