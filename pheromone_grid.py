from dataclasses import dataclass
from math import prod

DIFFUSIONEDGE = 1
DIFFUSIONCORNER = 1
DIFFUSIONMIDDLE = 1
DECAYSTRENGTH = 0.1

DIFFUSIONSTRENGTHSUM = 4 * DIFFUSIONCORNER + 4 * DIFFUSIONEDGE + DIFFUSIONMIDDLE
DIFFUSIONBLEED = (
    (1-DECAYSTRENGTH)*DIFFUSIONCORNER/DIFFUSIONSTRENGTHSUM,
    (1-DECAYSTRENGTH)*DIFFUSIONEDGE/DIFFUSIONSTRENGTHSUM,
    (1-DECAYSTRENGTH)*DIFFUSIONMIDDLE/DIFFUSIONSTRENGTHSUM)


@dataclass
class PheromoneGrid:
    time: float
    timer: float
    grid_list: list[tuple[float, float]]
    cell_size: tuple[int, int]
    grid_size: tuple[int, int]

    def __init__(self, screen_size: tuple[int, int]):
        self.time = 1
        self.timer = 0
        self.cell_size = (20, 20)
        self.grid_size = (
            screen_size[0]//self.cell_size[0], screen_size[1]//self.cell_size[1])
        self.grid_list = [(0, 0)] * prod(self.grid_size)


def pheromone_grid_system(obj: PheromoneGrid, dt: float):
    obj.timer += dt

    if obj.timer > obj.time:
        obj.timer = obj.timer % obj.time


def get_grid_neighbours(index: int, grid_size: tuple[int, int]) -> tuple[list[int], list[int], list[int]]:

    not_top: bool = index >= grid_size[0]
    not_bottom: bool = index <= grid_size[0]*(grid_size[1]-1)
    not_left: bool = index % grid_size[0] != 0
    not_right: bool = (index+1) % grid_size[0] != 0

    neighbour_to_add: list[bool] = [
        not_left and not_top   ,     not_top   ,     not_right and not_top   ,

        not_left               ,     False     ,     not_right               ,

        not_left and not_bottom,     not_bottom,     not_right and not_bottom]
    

    neighbour_corners: list[int] = []
    neighbour_edges: list[int] = []

    for x in range(9):
        if neighbour_to_add[x]:
            if x in [0, 2, 6, 8]:
                neighbour_corners.append(index+x % 3-1+(x//3-1)*grid_size[0])
            else:
                neighbour_edges.append(index+x % 3-1+(x//3-1)*grid_size[0])
    return (neighbour_corners, neighbour_edges, [index])



l: list[int]=[1,2,3]
l=[l[0]+x for x in l]
print(l)