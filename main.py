from random import randrange
import funcs as fc

if __name__ == '__main__':
    graph = fc.create_graph()
    for time in range(0, 1440, 10):
        graph.time = time
        graph.save_route('E', 'R', './figures/E_to_R/time={}.png'.format(time))
    '''
    graph.time = randrange(0, 1440)
    graph.show_route('E', 'R')
    '''