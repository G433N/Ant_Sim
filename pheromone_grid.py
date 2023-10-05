from dataclasses import dataclass
from math import prod

from typing import Final
from main import SCREEN_SIZE

TIME: Final = 1
DIFFUSION_EDGE: Final = 10
DIFFUSION_CORNER: Final = 5
DIFFUSION_MIDDLE: Final = 250
DECAY_STRENGTH: Final = 0.03
CELL_SIZE: Final = 20


def DIFFUSION_STRENGTH_SUM(corner: int, edge: int):
    return corner * DIFFUSION_CORNER + edge * DIFFUSION_EDGE + DIFFUSION_MIDDLE


GRID_SIZE: Final = (SCREEN_SIZE[0]//CELL_SIZE, SCREEN_SIZE[1]//CELL_SIZE)
DIFFUSIONBLEED: Final = (
    (1-DECAY_STRENGTH)*DIFFUSION_CORNER/DIFFUSION_STRENGTH_SUM(4, 4),
    (1-DECAY_STRENGTH)*DIFFUSION_EDGE/DIFFUSION_STRENGTH_SUM(4, 4),
    (1-DECAY_STRENGTH)*DIFFUSION_MIDDLE/DIFFUSION_STRENGTH_SUM(4, 4))


@dataclass
class PheromoneGrid:
    timer: float
    grid_list: list[float]
    grid_size: tuple[int, int]

    def __init__(self, grid_size: tuple[int, int] = GRID_SIZE):
        self.timer = 0
        self.grid_list = [0] * prod(grid_size)
        self.grid_size = grid_size

    def update(self, dt: float):
        self.timer += dt

        if self.timer >= TIME:
            self.timer = self.timer % TIME
            self.grid_list = self.get_diffused_list()

    def __str__(self):
        s = ""
        for i, x in enumerate(self.grid_list):
            b = (self.grid_size[0]-i-1) % self.grid_size[0] == 0
            s += f"{round(x, 3): <7}" + 2 * "\n" * b
        return s + f"\n{self.sum()}"

    def get_diffused_list(self):
        new_grid_list: list[float] = []
        grid = self.grid_list
        for i in range(prod(self.grid_size)):
            corner, edge = self.get_grid_neighbours(i)
            new_grid_list.append(
                sum(
                    (
                        sum(
                            diffusion_cal(grid[j], 0) for j in corner
                        ),
                        sum(
                            diffusion_cal(grid[j], 1) for j in edge
                        ),
                        diffusion_cal(grid[i], 2)
                    )
                )
            )

        return new_grid_list

    def get_grid_neighbours(self, index: int):

        not_top: bool = index >= self.grid_size[0]
        not_bottom: bool = index <= self.grid_size[0]*(self.grid_size[1]-2)
        not_left: bool = index % self.grid_size[0] != 0
        not_right: bool = (index+1) % self.grid_size[0] != 0

        neighbour_to_add: tuple[bool, ...] = (
            not_left and not_top,       not_top,    not_right and not_top,

            not_left,                   False,      not_right,

            not_left and not_bottom,    not_bottom, not_right and not_bottom
        )

        neighbour_corners: list[int] = []
        neighbour_edges: list[int] = []

        for x in range(9):
            if neighbour_to_add[x]:
                if x % 2 == 0:
                    neighbour_corners.append(
                        index+x % 3-1+(x//3-1)*self.grid_size[0])
                else:
                    neighbour_edges.append(
                        index+x % 3-1+(x//3-1)*self.grid_size[0])
        return neighbour_corners, neighbour_edges

    def sum(self):
        return sum(self.grid_list)


def diffusion_cal(grid: float, diff_index: int):
    return grid*DIFFUSIONBLEED[diff_index]


pg = PheromoneGrid((10, 10))
pg.grid_list[25] = 10
pg.grid_list[80] = 10
print(pg)
for _ in range(1):
    pg.update(TIME)
    print(pg)
