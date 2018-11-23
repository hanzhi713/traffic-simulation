import random
import networkx as nx
from cross import *

def determine_orientation(x : int, cross_road : CrossRoad, col : int = 2):
    """
    Determines which orientation (n, s, w, or e) the car should exit from the destination crossroad
    :param x: index of node in graph
    :param cross_road: the destination crossroad
    :param col:
    :return:
    """
    if x < col:
        return cross_road.north
    elif x % col == 0:
        return cross_road.west
    elif (x + 1) % col == 0:
        return cross_road.east
    else:
        return cross_road.south


def generate_cars(cross_roads : list, G, col :int = 2, row : int = -1, num_cars : int = 2, max_dist : int = 5):
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
        path = nx.shortest_path(G, ini, fi)

        out = determine_orientation(fi, cross_roads[fi], col)

        all_car.append(Car(random.randint(0, max_dist), cross_roads[ini], out, path))

    return all_car

def generate_node(num: int = 2):
    """
    :param num:
    :return:
    """
    cross_roads = [CrossRoad(bool(random.randint(0, 1)), bool(random.randint(0, 1))) for i in range(num ** 2)]
    return cross_roads

def generate_edge(cross_roads : list, num : int = 2):
    """
    :param cross_roads:
    :param num:
    :return:
    """

    gph = nx.DiGraph()

    for i in range(num ** 2):


        if num - i%num == 1 and i//num == num - 1:
            pass
        elif num - i%num == 1:
            gph.add_edge(cross_roads[i], cross_roads[i + num], length='10', dest=cross_roads[i + num].north)
            gph.add_edge(cross_roads[i + num], cross_roads[i], length='10', dest=cross_roads[i].south)
            pass
        elif i // num == num - 1:
            gph.add_edge(cross_roads[i], cross_roads[i + 1], length='10', dest=cross_roads[i + 1].west)
            gph.add_edge(cross_roads[i + 1], cross_roads[i], length='10', dest=cross_roads[i].east)
            pass
        else:
            gph.add_edge(cross_roads[i], cross_roads[i + 1], length='10', dest=cross_roads[i + 1].west)
            gph.add_edge(cross_roads[i + 1], cross_roads[i], length='10', dest=cross_roads[i].east)
            gph.add_edge(cross_roads[i], cross_roads[i + num], length='10', dest=cross_roads[i + num].north)
            gph.add_edge(cross_roads[i + num], cross_roads[i], length='10', dest=cross_roads[i].south)
        pass
    return gph