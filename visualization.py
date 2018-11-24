import networkx as nx
import pygame, sys

pygame.init()

def draw_cross(cross_roads : list, G : nx.DiGraph, col : int, row :int, cross_length = 50, scaling_factor : int = 10):

    hori_len = [G[cross_roads[i]][cross_roads[i+1]["length"]] for i in range(0, col - 1)]
    verti_len = [ G[cross_roads[i * col]][cross_roads[(i + 1) * col]]["length"] for i in range(0, row-1)]

    #a list that stores the information of the streets as grid

    sf = scaling_factor

    for i in range(0, )
        pass
    pass


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
