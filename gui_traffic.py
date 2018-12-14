import pygame
import car_coordination_improve
import generators
import cross as c
import networkx as nx
from typing import *

white = [255, 255, 255]
red = [255, 0, 0]
blue = [0, 0, 255]
yellow = [255, 255, 0]
green = [0, 255, 0]
pink = [255, 192, 203]


def create_crosses(row: int, column: int, cr_width: int, cr_height: int, street_width_x: int, street_width_y: int) -> \
        List[pygame.Rect]:
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


def create_streets(crosses: List[pygame.Rect], row: int, column: int, screen_size_x: int, screen_size_y: int) -> List[
    pygame.Rect]:
    """
    To get all the coordination of the streets in a list.
    Use polygon to connect all adjacent crosses
    :return: a list contains all the streets coordinations
    """
    streets = []
    # draw all horizontal
    for cross_num in range(len(crosses)):
        if (cross_num + 1) % column == 1:
            # use polygon to draw all the leftmost sides of crossroads

            pointlist = [(0, crosses[cross_num].y),
                         (crosses[cross_num].x, crosses[cross_num].y),
                         (crosses[cross_num].x, crosses[cross_num].y + crosses[cross_num].height),
                         (0, crosses[cross_num].y + crosses[cross_num].height)]
            streets.append(pygame.draw.polygon(screen, yellow, pointlist))

        if (cross_num + 1) % column == 0:
            # use polygon to draw all the rightmost side of crossroads

            pointlist = [(screen_size_x, crosses[cross_num].y),
                         (crosses[cross_num].x, crosses[cross_num].y),
                         (crosses[cross_num].x, crosses[cross_num].y + crosses[cross_num].height),
                         (screen_size_x, crosses[cross_num].y + crosses[cross_num].height)]
            streets.append(pygame.draw.polygon(screen, yellow, pointlist))

        if (cross_num + 1) % column != 0:
            # use polygon to connect all horizontal crossroads inside

            pointlist = [(crosses[cross_num].x + crosses[cross_num].width, crosses[cross_num].y),
                         (crosses[cross_num + 1].x, crosses[cross_num + 1].y),
                         (crosses[cross_num + 1].x, crosses[cross_num + 1].y + crosses[cross_num + 1].height),
                         (crosses[cross_num].x + crosses[cross_num].width,
                          crosses[cross_num].y + crosses[cross_num].height)]
            streets.append(pygame.draw.polygon(screen, yellow, pointlist))

    # draw all vertical
    for cross_num in range(len(crosses)):
        if cross_num < column:
            # use polygon to draw all the uppermost sides of crossroads

            pointlist = [(crosses[cross_num].x, 0),
                         (crosses[cross_num].x, crosses[cross_num].y),
                         (crosses[cross_num].x + crosses[cross_num].width, crosses[cross_num].y),
                         (crosses[cross_num].x + crosses[cross_num].width, 0)]
            streets.append(pygame.draw.polygon(screen, yellow, pointlist))

        if cross_num >= column * (row - 1):
            # use polygon to draw all the lowermost sides of crossroads

            pointlist = [(crosses[cross_num].x, screen_size_y),
                         (crosses[cross_num].x, crosses[cross_num].y),
                         (crosses[cross_num].x + crosses[cross_num].width, crosses[cross_num].y),
                         (crosses[cross_num].x + crosses[cross_num].width, screen_size_y)]
            streets.append(pygame.draw.polygon(screen, yellow, pointlist))

        if cross_num < column * (row - 1):
            # use polygon to connect all vertical crossroads inside

            pointlist = [(crosses[cross_num].x, crosses[cross_num].y + crosses[cross_num].height),
                         (crosses[cross_num].x + crosses[cross_num].width,
                          crosses[cross_num].y + crosses[cross_num].height),
                         (crosses[cross_num + column].x + crosses[cross_num + column].width,
                          crosses[cross_num + column].y),
                         (crosses[cross_num + column].x,
                          crosses[cross_num + column].y)]
            streets.append(pygame.draw.polygon(screen, yellow, pointlist))

    return streets


def draw_lights(screen: pygame.Surface, cross_rect: pygame.Rect, cross_road: c.CrossRoad, light_offset: List):
    """
    Draw individual light according to each cross road status
    :param screen:
    :param cross_rect:
    :param cross_road:
    :param light_offset:
    :return: None
    """
    ns_light = [light_offset[0], light_offset[1] // 3]
    we_light = [light_offset[0] // 3, light_offset[1]]
    if cross_road.ns_state:
        screen.fill(green, cross_rect.inflate(*ns_light))
    else:
        screen.fill(red, cross_rect.inflate(*ns_light))
    if cross_road.we_state:
        screen.fill(green, cross_rect.inflate(*we_light))
    else:
        screen.fill(red, cross_rect.inflate(*we_light))


def move_car(G: nx.DiGraph, cross_roads: List[c.CrossRoad], all_car: List[c.Car]):
    """
    call the cross program and update the system
    :return: None
    """
    c.update(G, all_car, cross_roads, 1)


def main(screen: pygame.Surface, G: nx.DiGraph, cross_roads: List[c.CrossRoad], all_car: List[c.Car],
         crosses: List[pygame.Rect],
         streets: List[pygame.Rect],
         light_offset: List):
    pygame.init()
    font = pygame.font.SysFont('Arial', 10)
    clock = pygame.time.Clock()

    while True:
        remove_count = 0
        while True:
            if all_car[remove_count].arrived:
                all_car.pop(remove_count)
            else:
                remove_count += 1
            if remove_count >= len(all_car):
                break

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break

        screen.fill(white)  # the background
        for i in streets:
            screen.fill(yellow, i)  # the streets
        for count, i in enumerate(crosses):
            screen.fill(blue, i)  # the crossroads
            draw_lights(screen, i, cross_roads[count], light_offset)  # draw the lights according to its state

        for count, i in enumerate(all_car, 1):  # all the car locations
            i.location = car_coordination_improve.get_the_location(crosses, cross_roads, i,
                                                                   car_length)  # init to cross need to improve
            print(i.location, i.dist_to_cross)

            car_num = font.render(str(count), True, [0, 0, 0])
            screen.fill(pink, i.location)
            screen.blit(car_num, i.location)

        pygame.display.flip()
        move_car(G, cross_roads, all_car)
        clock.tick(4)
        print("Divider: *********************************")


if __name__ == "__main__":
    """
    set all the parameters
    """

    screen_size_x = 800
    screen_size_y = 800
    column = 3
    row = 4
    screen = pygame.display.set_mode([screen_size_x, screen_size_y])
    cr_width = 50
    cr_height = 50
    light_offset = [-cr_width * 4 // 5, -cr_height * 4 // 5]
    street_width_x = (screen_size_x - column * cr_width) // (column + 1)
    street_width_y = (screen_size_y - row * cr_height) // (row + 1)
    car_length = 10

    """Get the location of crossroad and street in pygame.Rect. Ready to draw them"""
    crosses = create_crosses(row, column, cr_width, cr_height, street_width_x, street_width_y)
    streets = create_streets(crosses, row, column, screen_size_x, screen_size_y)

    """Generate the crossroad objects, the graph, and all the car objects"""
    cross_roads = generators.generate_node(col=column, row=row, red_prob=1)
    G = generators.generate_edge(cross_roads, col=column, row=row)
    all_car = generators.generate_cars(cross_roads, G, col=column, row=row, num_cars=1)

    main(screen, G, cross_roads, all_car, crosses, streets, light_offset)
