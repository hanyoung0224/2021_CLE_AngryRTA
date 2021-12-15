from random import randrange
import funcs as fc

if __name__ == '__main__':
    graph = fc.create_graph()

    for time in range(0, 1440, 10):
        graph.time = time
        graph.save_route('N', 'A', './figures/N_to_A/time={}.png'.format(time))
