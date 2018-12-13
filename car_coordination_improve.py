from cross import *
import networkx as nx
from cross import Car
import pygame

def get_the_location(crosses, cross_roads: List[CrossRoad], car: Car, car_length: int = 10):
    # problem: at the end, there is no node, so action[0] will be an error but it may not reach the destination
    # initial_distance is the original distance to the first node. It is constant
    #  column shi xiang xia
    # the initial edge distance
    # edge_length_x = 50  # the initial edge length/ the non-connected part
    # edge_length_y = 50  # the initial edge length/ the non-connected part
    try:
        location = [-1, -1]
        dis_betw_car = 2
        # find the crossroad location
        for count, node in enumerate(cross_roads):
            if node is car.actions[0]:
                location[0] = count
                break
        print(location[0])
        # find the queue location
        for count, direction in enumerate(car.actions[0].all):
            if car.dest is direction:
                location[1] = count
                break
        # uses the cross to find the origin, the middle
        origin = pygame.Rect(crosses[location[0]].x + crosses[location[0]].width // 2 - car_length // 2,
                             crosses[location[0]].y + crosses[location[0]].height // 2 - - car_length // 2, car_length,
                             car_length)
        # check if the car is in pass in progress
        if car in car.actions[0].pass_in_prog:
            return origin

        # find the location of the car if it is on one of the edges, the algo should be good
        if location[1] != -1:
            if location[1] == 0:
                # it is north
                origin.y -= 0.5 * car_length - car.dist_to_cross * (car_length + dis_betw_car) + - crosses[
                    location[0]].height // 2
                return origin
            elif location[1] == 1:
                # it is south
                origin.y += 0.5 * car_length + car.dist_to_cross * (car_length + dis_betw_car) + crosses[
                    location[0]].height // 2
                return origin
            elif location[1] == 2:
                # it is west
                origin.x -= 0.5 * car_length - car.dist_to_cross * (car_length + dis_betw_car) - crosses[
                    location[0]].width // 2
                return origin
            elif location[1] == 3:
                # it is east
                origin.x += 0.5 * car_length + car.dist_to_cross * (car_length + dis_betw_car) + crosses[
                    location[0]].width // 2
                return origin
        else:
            print("cant find which edge it is on")
    except IndexError:
        print("ACTION Index Error?")


if __name__ == "__main__":
    screen_sz = 800
