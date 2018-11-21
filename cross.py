import random
import networkx as nx


class CrossRoad:
    def __init__(self, ns_state, we_state):
        self.west = []
        self.east = []
        self.north = []
        self.south = []
        self.all = [self.north, self.south, self.west, self.east]
        self.pass_in_prog = {}
        self.ns_state = ns_state
        self.we_state = we_state


class Car:
    def __init__(self, init_dist: int, cross_road: CrossRoad, init_dest: list, actions: list):
        self.wait_time = 0
        self.dest = init_dest
        self.current_cross = cross_road
        self.dist_to_cross = init_dist
        self.actions = actions
        self.cross_time = 2
        self.updated = False
        self.arrived = False
    #
    # def draw(self, x, y, w, h, screen, color=(255, 255, 255)):
    #     pygame.draw.rect(screen, color, (x, y, w, h))


G = nx.DiGraph()
cross_roads = [CrossRoad(bool(random.randint(0, 1)), bool(random.randint(0, 1))) for i in range(9)]
all_cars = [
    Car(
        2, cross_roads[1], cross_roads[3].north, [cross_roads[3], cross_roads[4]]
    ),
    Car(
        3, cross_roads[4], cross_roads[2].south, [cross_roads[2], cross_roads[1]]
    )
]

G.add_edge(cross_roads[0], cross_roads[1], length='10', dest=cross_roads[1].west)
G.add_edge(cross_roads[1], cross_roads[0], length='10', dest=cross_roads[0].east)
G.add_edge(cross_roads[0], cross_roads[2], length='10', dest=cross_roads[2].north)
G.add_edge(cross_roads[2], cross_roads[0], length='10', dest=cross_roads[2].south)
G.add_edge(cross_roads[1], cross_roads[3], length='10', dest=cross_roads[3].north)
G.add_edge(cross_roads[3], cross_roads[1], length='10', dest=cross_roads[1].south)
G.add_edge(cross_roads[3], cross_roads[2], length='10', dest=cross_roads[2].east)
G.add_edge(cross_roads[2], cross_roads[3], length='10', dest=cross_roads[3].west)


def update_cross_roads(time: int = 1):
    """
    :param time: the global time step
    :return: None
    """
    for cross_road in cross_roads:
        # update pass_in_progress
        # assuming pass_in_prog has unlimited capacity
        for car in cross_road.pass_in_prog.keys():

            # increase the time that each car has spent passing the cross road
            cross_road.pass_in_prog[car] += time
            car.updated = True

            # if the time spent is greater than the predefined cross time,
            # then the car has already passed the cross road.
            if cross_road.pass_in_prog[car] >= car.cross_time:
                # remove the car from the pass in progress dictionary
                cross_road.pass_in_prog.pop(car)

                # if the car has not yet arrived at its final destination
                if len(car.actions) > 0:
                    # place the car on the way to the next cross road
                    car.current_cross = car.actions.pop(0)

                    # get the edge from the past cross road to the next cross road
                    edge = G[cross_road][car.current_cross]

                    # update the car's distance to the next cross road
                    car.dist_to_cross = edge['length']

                    # update car's reference to the next cross road's queue
                    car.dest = edge['dest']
                else:
                    car.arrived = True

        # then, update the queue of cars waiting to pass
        # if the cars are in the queues of north-south direction
        if cross_road.ns_state:
            for queue in cross_road.all[:2]:
                if len(queue) == 0:
                    continue

                # remove the front car from the waiting list
                current_car = queue.pop(0)
                current_car.updated = True

                # put the car in the pass in progress dict and set the time
                cross_road.pass_in_prog[current_car] = time

        # if the cars are in the queues of west-east direction
        elif cross_road.we_state:
            for queue in cross_road.all[2:]:
                if len(queue) == 0:
                    continue
                current_car = queue.pop(0)
                current_car.updated = True
                cross_road.pass_in_prog[current_car] = time


def update_all_cars(time: int):
    """
    :param time: the global time step
    :return:
    Assumption: All cars' velocities are 1
                The length of each car is 1
                The length of the street is measured using car length
    Warning: Must be executed after update_cross_roads
    """
    for car in all_cars:

        if car.arrived:
            continue

        # if the car has not been updated by the update_cross_roads method
        # namely, the car is not in the waiting queue or the pass in progress dict
        if not car.updated:
            # that means the car is on the way to the next queue
            # update the distance by the amount of time
            car.dist_to_cross -= time

        # if the car's distance to the next cross road is smaller than the length of the queue,
        # that means the car has reached the tail of the queue
        # and therefore we append the car to the queue
        if car.dist_to_cross <= len(car.dest) and car not in car.dest:
            car.dest.append(car)

        # clear the flag for the next update
        car.updated = False

        car.wait_time += time


def update(time):
    update_cross_roads(time)
    update_all_cars(time)


#     policy()
#
# def policy():
#     cross_roads[0].ns_state = True
#

if __name__ == "__main__":
    for i in range(100):
        print(i)
        update(1)
