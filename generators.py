import random
import networkx as nx
from cross import *


def generate_cars(cross_roads: List[CrossRoad], G: nx.DiGraph, col: int = 2, row: int = -1, num_cars: int = 2,
                  max_dist: int = 5) -> List[Car]:
    """
    :param cross_roads: list of crossroads (nodes of the graph)
    :param G: the graph
    :param col:
    :param row:
    :param num_cars:
    :param max_dist: maximum distance from the first crossroad the car would pass
    :return: list of cars
    """

    row = col if row == -1 else row

    ini_fi_points = [i for i in range(0, col)]
    ini_fi_points.extend([i * col for i in range(1, row - 1)])
    ini_fi_points.extend([(i + 1) * col - 1 for i in range(1, row - 1)])
    ini_fi_points.extend([i for i in range(col * (row - 1), col * row)])

    num_init_point = len(ini_fi_points)

    all_car = []

    for i in range(num_cars):
        inf = random.sample(range(0, num_init_point), 2)
        ini = ini_fi_points[inf[0]]
        fi = ini_fi_points[inf[1]]
        path = nx.shortest_path(G, cross_roads[ini], cross_roads[fi])

        if ini < col:
            destination = cross_roads[ini].north
        elif col * (row - 1) <= ini < col * row:
            destination = cross_roads[ini].south
        elif ini in [i * col for i in range(1, row - 1)]:
            destination = cross_roads[ini].west
        else:
            destination = cross_roads[ini].east

        all_car.append(Car(random.randint(0, max_dist), destination, path))

    return all_car


def generate_node(col: int = 2, row: int = -1, red_prob: int = 0.5) -> List[CrossRoad]:
    """
    :param col:
    :param row:
    :return:
    """
    row = col if row == -1 else row
    rand_float = random.random()
    red = True if rand_float > red_prob else False
    cross_roads = [CrossRoad(red, not red) for i in range(col * row)]
    return cross_roads


def generate_edge(cross_roads: list, col: int = 2, row: int = -1, len_lb: int = 10, len_ub: int = 10) -> nx.DiGraph:
    """
    :param cross_roads:
    :param num:
    :return:
    """
    row = col if row == -1 else row
    hori_len = [random.randint(len_lb, len_ub) for i in range(0, col - 1)]
    verti_len = [random.randint(len_lb, len_ub) for i in range(0, row - 1)]

    gph = nx.DiGraph()

    for i in range(col * row):
        if (i + 1) % col == 0 and i // col == row - 1:
            pass
        elif col - i % col == 1:
            # rightmost
            gph.add_edge(cross_roads[i], cross_roads[i + col], length=verti_len[i // col],
                         dest=cross_roads[i + col].north)
            gph.add_edge(cross_roads[i + col], cross_roads[i],
                         length=verti_len[i // col], dest=cross_roads[i].south)
        elif i // col == row - 1:
            # bottom
            gph.add_edge(cross_roads[i], cross_roads[i + 1],
                         length=hori_len[i % col], dest=cross_roads[i + 1].west)
            gph.add_edge(cross_roads[i + 1], cross_roads[i],
                         length=hori_len[i % col], dest=cross_roads[i].east)
        else:
            gph.add_edge(cross_roads[i], cross_roads[i + 1],
                         length=hori_len[i % col], dest=cross_roads[i + 1].west)
            gph.add_edge(cross_roads[i + 1], cross_roads[i],
                         length=hori_len[i % col], dest=cross_roads[i].east)
            gph.add_edge(cross_roads[i], cross_roads[i + col], length=verti_len[i // col],
                         dest=cross_roads[i + col].north)
            gph.add_edge(cross_roads[i + col], cross_roads[i],
                         length=verti_len[i // col], dest=cross_roads[i].south)
    return gph
