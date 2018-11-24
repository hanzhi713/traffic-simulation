from GUI.cross import *
import networkx as nx
from cross import Car


def get_the_location(G: nx.connected_components, crossroads: list, car: Car, column1: int, row1: int):
    # problem: at the end, there is no node, so action[0] will be an error but it may not reach the destination
    # initial_distance is the original distance to the first node. It is constant
    #  column shi xiang xia
    # the initial edge distance
    edge_length_x = 50 # the initial edge length/ the non-connected part
    edge_length_y = 50 # the initial edge length/ the non-connected part
    location = [-1, -1]

    # find the crossroad location
    for count, node in enumerate(cross_roads, 1):
        if node is car.actions[0]:
            location[0] = count
            break

    # find the queue location
    for count, direction in enumerate(car.actions[0].all):
        if car.dest is direction:
            location[1] = count
            break

    # get how many rows and columns the car is at
    row = location[0] // column1 + 1
    column = location[0] % column1 + 1

    # the edge length is the sum of the edges in x direction
    for i in range(column - 1): # there are (column - 1) edges connected before the node
        edge_length_x += G[cross_roads[(row - 1) * column1 + i]][cross_roads[(row - 1) * column1 + i + 1]]['length']

    # the edge length is the sum of the edges in y direction
    for i in range(row - 1): # # there are (row - 1) edges connected before the node
        edge_length_y += G[cross_roads[(column - 1) * row1 + i]][cross_roads[(column - 1) * row1 + i + 1]]['length']

    origin = [edge_length_x + (column - 1) * cross_road_length_x + 0.5 * cross_road_length_x,
              edge_length_y + (row - 1) * cross_road_length_y + 0.5 * cross_road_length_y]

    # check if the car is in pass in progress
    if car in car.actions[0].pass_in_prog:
        return origin

    # find the location of the car if it is on one of the edges
    if location[1] != -1:
        if location[1] == 0:
            # it is north
            origin[1] -= 0.5 * car_length + car.dist_to_cross * car_length
            return origin
        elif location[1] == 1:
            # it is south
            origin[1] += 0.5 * car_length + car.dist_to_cross * car_length
            return origin
        elif location[1] == 2:
            # it is west
            origin[0] -= 0.5 * car_length + car.dist_to_cross * car_length
            return origin
        elif location[1] == 3:
            # it is east
            origin[0] += 0.5 * car_length + car.dist_to_cross * car_length
            return origin


if __name__ == "__main__":
    screen_sz = 800
    car_length = 10  # the side length
    cross_road_length_x = 50
    cross_road_length_y = 50
