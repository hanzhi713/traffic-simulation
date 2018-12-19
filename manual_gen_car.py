import random
from cross import *


def generate_cars(init_dist: List[Union[int, float]], init_dest: List[list], actions: List[list], num_cars: int = 1) -> \
List[Car]:
    all_cars = []
    for i in range(num_cars):
        dist = init_dist[i]
        destination = init_dest[i]
        path = actions[i]
        all_cars.append(Car(dist, destination, path))

    return all_cars


def generate_node(col: int = 2, row: int = -1, red_prob: float = 0.5) -> List[CrossRoad]:
    """
    :param col:
    :param row:
    :return:
    """
    row = col if row == -1 else row
    red = True if random.random() > red_prob else False
    return [CrossRoad(red, not red) for i in range(col * row)]


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
