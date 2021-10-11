from graph import Graph


node_locations = [
    (0, 0),
    (0, 270),
    (0, 470),
    (0, 850),
    (0, 1020),
    (-170, 230),
    (-170, 470),
    (-210, 0),
    (-270, 820),
    (-310, 1000),
    (-320, 380),
    (-410, 220),
    (-430, 0),
    (-600, 640),
    (-760, 320),
    (-780, 0),
    (-780, 70),
    (-890, 40),
    (-980, 0),
]

node_edges = [
    ('A', 'B'),
    ('B', 'C'),
    ('C', 'D'),
    ('D', 'E'),
    ('B', 'F'),
    ('F', 'H'),
    ('A', 'H'),
    ('F', 'K'),
    ('C', 'G'),
    ('G', 'K'),
    ('K', 'L'),
    ('L', 'M'),
    ('H', 'M'),
    ('G', 'I'),
    ('L', 'O'),
    ('D', 'I'),
    ('I', 'N'),
    ('N', 'O'),
    ('O', 'Q'),
    ('Q', 'P'),
    ('M', 'P'),
    ('P', 'S'),
    ('E', 'J'),
    ('I', 'J')
]

node_edges_onedir = [
    ('S', 'R'),
    ('R', 'Q')
]

if __name__ == '__main__':
    graph = Graph()
    for i, loc in enumerate(node_locations):
        graph.add_node(chr(i + 65), loc)
    for x, y in node_edges:
        graph.add_edge(x, y)
        graph.add_edge(y, x)
    for x, y in node_edges_onedir:
        graph.add_edge(x, y)
    graph.show_route('R', 'C')
