import pygame
import car_coordination_improve
import manual_gen_car
from cross import nx, World, CrossRoad, Car
from policies import tl_global_const
from typing import *

white = [255, 255, 255]
red = [255, 0, 0]
blue = [0, 0, 255]
yellow = [255, 255, 0]
green = [0, 255, 0]
pink = [255, 192, 203]


def create_crosses(row: int, column: int, cr_width: int, cr_height: int,
                   street_width_x: int, street_width_y: int) -> List[pygame.Rect]:
    """
    To get all the coordination of the crossroads in a list
    :return: a list contains all the crossroads coordinations
    """
    crosses = []
    for i in range(row):
        for j in range(column):
            crosses.append(pygame.Rect(
                street_width_x * (j + 1) + j * cr_width,
                street_width_y * (i + 1) + i * cr_height,
                cr_width, cr_height))
    print("cross 0 is", crosses[0].x, crosses[0].y)
    return crosses


def create_streets(crosses: List[pygame.Rect], row: int, column: int,
                   screen_size_x: int, screen_size_y: int) -> List[pygame.Rect]:
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
                         (crosses[cross_num].x, crosses[cross_num].y +
                          crosses[cross_num].height),
                         (0, crosses[cross_num].y + crosses[cross_num].height)]
            streets.append(pygame.draw.polygon(screen, yellow, pointlist))

        if (cross_num + 1) % column == 0:
            # use polygon to draw all the rightmost side of crossroads

            pointlist = [(screen_size_x, crosses[cross_num].y),
                         (crosses[cross_num].x, crosses[cross_num].y),
                         (crosses[cross_num].x, crosses[cross_num].y +
                          crosses[cross_num].height),
                         (screen_size_x, crosses[cross_num].y + crosses[cross_num].height)]
            streets.append(pygame.draw.polygon(screen, yellow, pointlist))

        if (cross_num + 1) % column != 0:
            # use polygon to connect all horizontal crossroads inside

            pointlist = [(crosses[cross_num].x + crosses[cross_num].width, crosses[cross_num].y),
                         (crosses[cross_num + 1].x, crosses[cross_num + 1].y),
                         (crosses[cross_num + 1].x, crosses[cross_num +
                                                            1].y + crosses[cross_num + 1].height),
                         (crosses[cross_num].x + crosses[cross_num].width,
                          crosses[cross_num].y + crosses[cross_num].height)]
            streets.append(pygame.draw.polygon(screen, yellow, pointlist))

    # draw all vertical
    for cross_num in range(len(crosses)):
        if cross_num < column:
            # use polygon to draw all the uppermost sides of crossroads

            pointlist = [(crosses[cross_num].x, 0),
                         (crosses[cross_num].x, crosses[cross_num].y),
                         (crosses[cross_num].x +
                          crosses[cross_num].width, crosses[cross_num].y),
                         (crosses[cross_num].x + crosses[cross_num].width, 0)]
            streets.append(pygame.draw.polygon(screen, yellow, pointlist))

        if cross_num >= column * (row - 1):
            # use polygon to draw all the lowermost sides of crossroads

            pointlist = [(crosses[cross_num].x, screen_size_y),
                         (crosses[cross_num].x, crosses[cross_num].y),
                         (crosses[cross_num].x +
                          crosses[cross_num].width, crosses[cross_num].y),
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


def draw_lights(screen: pygame.Surface, cross_rect: pygame.Rect,
                cross_road: CrossRoad, light_offset: List[int]) -> None:
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


def main(screen: pygame.Surface, column: int, row: int, G: nx.DiGraph, cross_roads: List[CrossRoad],
         all_cars: List[Car],
         crosses: List[pygame.Rect], streets: List[pygame.Rect], light_offset: List[int]) -> None:
    """
    The main method
    """
    pygame.init()
    font = pygame.font.SysFont('Arial', 10)
    clock = pygame.time.Clock()

    world = World(G, cross_roads, all_cars, tl_global_const)

    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            exit()

        screen.fill(white)  # the background
        for st in streets:
            screen.fill(yellow, st)  # the streets
        for i, cross in enumerate(crosses):
            screen.fill(blue, cross)  # the crossroads
            # draw the lights according to its state
            draw_lights(screen, cross, cross_roads[i], light_offset)

        for num, car in enumerate(all_cars, 1):  # all the car locations
            location = car_coordination_improve.get_the_location(crosses, cross_roads, car, column, row,
                                                                 car_length)  # init to cross need to improve
            print(location, car.dist_to_cross)

            car_num = font.render(str(num), True, [0, 0, 0])
            screen.fill(pink, location)
            screen.blit(car_num, location)
            # if location.y == 140:
            #     pygame.display.flip()
            #     input()

        pygame.display.flip()
        world.update_all(0.8)

        remove_count = 0
        while True:
            if all_cars[remove_count].arrived:
                all_cars.pop(remove_count)
            else:
                remove_count += 1
            if remove_count >= len(all_cars):
                break

        if len(all_cars) == 0:
            break

        clock.tick(2)
        print("Divider: *********************************")

    print("Simulation done")
    world.stats()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break


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
    car_num = 1

    """Get the location of crossroad and street in pygame.Rect. Ready to draw them"""
    crosses = create_crosses(row, column, cr_width,
                             cr_height, street_width_x, street_width_y)
    streets = create_streets(crosses, row, column,
                             screen_size_x, screen_size_y)

    """Generate the crossroad objects, the graph, and all the car objects"""
    cross_roads = manual_gen_car.generate_node(col=column, row=row, red_prob=1)
    G = manual_gen_car.generate_edge(cross_roads, col=column, row=row)

    """Here is all the parameter for generating a car"""
    init_dist = [10]
    init_dest = [cross_roads[0].north]
    actions = [[cross_roads[0], cross_roads[1], cross_roads[2]]]
    all_cars = manual_gen_car.generate_cars(init_dist, init_dest, actions)

    """MAIN PROGRAM"""
    main(screen, column, row, G, cross_roads, all_cars, crosses, streets, light_offset)
