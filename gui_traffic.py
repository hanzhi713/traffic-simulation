import pygame
import car_coordination_improve
import generators
import cross as c
import networkx as nx
from typing import *

white = [255, 255, 255]
red = [255, 0, 0]
blue = [0, 0, 255]


def create_crosses() -> List[pygame.Rect]:
    """
    To get all the coordination of the crossroads in a list
    :return: a list contains all the crossroads coordinations
    """
    crosses = []
    for i in range(row):
        for j in range(column):
            crosses.append(pygame.Rect(
                street_width_x * (j + 1) + j * cr_width, street_width_y * (i + 1) + i * cr_height,
                cr_width,
                cr_height))
    return crosses


def move_car(G: nx.DiGraph, cross_roads: List[c.CrossRoad], all_car: List[c.Car]):
    """
    call the cross program and update the system
    :return:
    """
    c.update(G, all_car, cross_roads, 1)


def main(G: nx.DiGraph, cross_roads: List[c.CrossRoad], all_car: List[c.Car], crosses: List[pygame.Rect]):
    pygame.init()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        screen.fill(white)  # the background
        for i in crosses:
            screen.fill(blue, i)  # the crossroads
        for count, i in enumerate(all_car, 1):  # all the car locations
            i.location = car_coordination_improve.get_the_location(crosses, cross_roads, i,
                                                                   car_length)  # init to cross need to improve
            print(i.location, i.dist_to_cross)

            car_num = font.render(str(count), True, [0, 0, 0])
            screen.fill(red, i.location)
            screen.blit(car_num, i.location)

        remove_count = 0
        while True:
            if all_car[remove_count].arrived:
                all_car.pop(remove_count)
            else:
                remove_count += 1
            if remove_count >= len(all_car):
                break

        pygame.display.flip()
        move_car(G, cross_roads, all_car)
        clock.tick(1)
        print("Divider: *********************************")
        # move_car(cross_roads, all_car)


if __name__ == "__main__":
    """
    set all the parameters
    """

    screen_size_x = 800
    screen_size_y = 800
    column = 5
    row = 5
    screen = pygame.display.set_mode([screen_size_x, screen_size_y])
    cr_width = 50
    cr_height = 50
    street_width_x = (screen_size_x - column * cr_width) // (column + 1)
    street_width_y = (screen_size_y - row * cr_height) // (row + 1)
    car_length = 10
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 10)

    """get the cross_roads and edges and cars ready!!"""
    crosses = create_crosses()
    cross_roads = generators.generate_node(col=column, row=row)
    G = generators.generate_edge(cross_roads, col=column, row=row)
    # import matplotlib.pyplot as plt
    # import networkx as nx
    # plt.figure()
    # nx.draw(G)
    # plt.show()
    all_car = generators.generate_cars(cross_roads, G, col=column, row=row, num_cars=1)

    main(G, cross_roads, all_car, crosses)
