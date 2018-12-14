from cross import nx, CrossRoad, Car
from typing import List

def tl_global_const(G: nx.DiGraph, all_cross_roads: List[CrossRoad], all_cars: List[Car], g_time: int) -> None:
    if g_time % 15 == 0:
        for cr in all_cross_roads:
            cr.we_state = not cr.we_state
            cr.ns_state = not cr.ns_state
