from dataclasses import dataclass
from math import prod

from typing import Final

from pygame import Color, Surface, Vector2
import pygame
from Util.globals import SCREEN_SIZE

TIME: Final = 0.4
DIFFUSION_EDGE: Final = 10
DIFFUSION_MIDDLE: Final = 100
CELL_SIZE: Final = 40
MAX_PER_TILE: Final = 255


def DIFFUSION_STRENGTH_SUM(edge: int):
    return edge * DIFFUSION_EDGE + DIFFUSION_MIDDLE


GRID_SIZE: Final = (SCREEN_SIZE[0]//CELL_SIZE, SCREEN_SIZE[1]//CELL_SIZE)

DIFFUSION_STRENGTH_MAP: Final = (DIFFUSION_STRENGTH_SUM(
    2), DIFFUSION_STRENGTH_SUM(3), DIFFUSION_STRENGTH_SUM(4))


@dataclass
class PheromoneGrid:
    timer: float
    grid_list: list[int]
    len: int

    def __init__(self):
        self.timer = 0
        self.len = prod(GRID_SIZE)
        self.grid_list = [0] * self.len

    def update(self, dt: float):
        self.timer += dt

        if self.timer >= TIME:
            self.timer = self.timer % TIME
            self.grid_list = get_diffused_list(self.grid_list)

    def add(self,
            position: Vector2,
            strenght: int = 100,
            grid_size: tuple[int, int] = GRID_SIZE,
            cell_size: int = CELL_SIZE
            ):
        x = int(position.x/cell_size)
        y = int(grid_size[0]*int(position.y/cell_size))
        index = x + y
        if 0 > index or self.len <= index:
            return
        self.grid_list[index] += strenght

    def __str__(self):
        s = ""
        for i, x in enumerate(self.grid_list):
            b = (GRID_SIZE[0]-i-1) % GRID_SIZE[0] == 0
            s += f"{round(x, 3): <7}" + 2 * "\n" * b
        return s + f"\n{self.sum()}"

    def draw(self, screen: Surface, grid_size: tuple[int, int] = GRID_SIZE):
        for y in range(grid_size[1]):
            for x in range(grid_size[0]):
                rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE,
                                   CELL_SIZE, CELL_SIZE)
                i = x+y*(grid_size[0])
                alpha = max(0, min(255, self.grid_list[i]))
                c = Color(240, 30, alpha)
                pygame.draw.rect(screen, c, rect)

    def sum(self):
        return sum(self.grid_list)


def get_diffused_list(grid_list: list[int], grid_size: tuple[int, int] = GRID_SIZE) -> list[int]:
    new_grid_list: list[int] = []

    for i in range(prod(grid_size)):
        s: int = grid_list[i]

        case: int = get_map_case(i)

        if (i >= grid_size[0]):
            """up"""
            s += diffusion_calc(grid_list, i, i - grid_size[0], case)

        if ((i+1) % grid_size[0]):
            """right"""
            s += diffusion_calc(grid_list, i, i + 1, case)

        if (i <= grid_size[0]*(grid_size[1]-2)):
            """down"""
            s += diffusion_calc(grid_list, i, i + grid_size[0], case)

        if (i % grid_size[0]):
            """left"""
            s += diffusion_calc(grid_list, i, i - 1, case)

        new_grid_list.append(min(s-(s >> 5), MAX_PER_TILE))

    return new_grid_list


def diffusion_calc(grid_list: list[int], index: int, neighbour_index: int, case: int) -> int:
    return ((DIFFUSION_EDGE * grid_list[neighbour_index])
            // DIFFUSION_STRENGTH_MAP[get_map_case(neighbour_index)]
            -
            (DIFFUSION_EDGE * grid_list[index])
            // DIFFUSION_STRENGTH_MAP[case])


def get_map_case(index: int, grid_size: tuple[int, int] = GRID_SIZE) -> int:
    top: bool = index < grid_size[0]
    bottom: bool = index > grid_size[0]*(grid_size[1]-2)
    left: bool = index % grid_size[0] == 0
    right: bool = (index+1) % grid_size[0] == 0

    match (left, top, right, bottom):
        case True, True, False, False:
            """Top_Left"""
            return 0

        case False, True, False, False:
            """"Top_Middle"""
            return 1

        case False, True, True, False:
            """"Top_Right"""
            return 0

        case True, False, False, False:
            """"Middle_Left"""
            return 1

        case False, False, False, False:
            """"Middle_Middle"""
            return 2

        case False, False, True, False:
            """"Middle_Right"""
            return 1

        case True, False, False, True:
            """"Bottom_Left"""
            return 0

        case False, False, False, True:
            """"Bottom_Middle"""
            return 1

        case False, False, True, True:
            """"Bottom_Right"""
            return 0

        case _:
            raise ValueError


def case_selection():
    num = 1
    for x in range(9):
        yield x, num
        num <<= 1

# pg = PheromoneGrid((10, 10))
# pg.grid_list[25] = 10
# pg.grid_list[80] = 10
# print(pg)
# for _ in range(1):
    # pg.update(TIME)
    # print(pg)
