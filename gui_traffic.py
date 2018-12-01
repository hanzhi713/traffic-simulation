import pygame
import car_coordination
import generator
import cross as c

white = [255, 255, 255]
red = [255, 0, 0]


def create_crosses():
    """
    To get all the coordination of the crossroads in a list
    :return: a list contains all the crossroads coordinations
    """
    crosses = []
    for i in range(row):
        for j in range(column):
            crosses.append(pygame.Rect(
                street_width_x * (j + 1) + j * cross_road_length_x, street_width_y * (i + 1) + i * cross_road_length_y,
                cross_road_length_x,
                cross_road_length_y))
    return crosses


def move_car():
    """
    call the cross program and update the system
    :return:
    """
    c.update(1)


def main():
    pygame.init()
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        screen.fill(white) # the background
        for i in crosses:
            screen.fill(red, i) # the crossroads
        for i in all_car: # all the car locations
            i.location = car_coordination.get_the_location(G, cross_roads, i, column, row)
            the_car = pygame.Rect(i.location[0] - 5, i.location[1] - 5, car_length, car_length)
            screen.fill(red, the_car)
        pygame.display.flip()
        move_car()


if __name__ == "__main__":
    """
    set all the parameters
    """

    screen_size_x = 800
    screen_size_y = 800
    column = 4
    row = 4
    screen = pygame.display.set_mode([screen_size_x, screen_size_y])
    cross_road_length_x = 50
    cross_road_length_y = 50
    street_width_x = (screen_size_x - column * cross_road_length_x) // (column + 1)
    street_width_y = (screen_size_y - row * cross_road_length_y) // (row + 1)
    car_length = 10

    """get the cross_roads and edges and cars ready!!"""
    crosses = create_crosses()
    cross_roads = generator.generate_node(16)
    G = generator.generate_edge(cross_roads, 4)
    all_car = generator.generate_cars(cross_roads, G, column) # there is something wrong here

    main()
