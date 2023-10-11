from dataclasses import dataclass
from math import prod

from typing import Final

from pygame import Color, Surface, Vector2
import pygame
from Util.globals import SCREEN_SIZE

DIFFUSION_TIME: Final = 0.05
DECAY_TIME: Final = 1

DIFFUSION_EDGE: Final = 1
DIFFUSION_MIDDLE: Final = 50
MAX_PER_TILE: Final = 2047


def DIFFUSION_STRENGTH_SUM(edge: int):
    return edge * DIFFUSION_EDGE + DIFFUSION_MIDDLE


DIFFUSION_STRENGTH_MAP: Final = (DIFFUSION_STRENGTH_SUM(
    2), DIFFUSION_STRENGTH_SUM(3), DIFFUSION_STRENGTH_SUM(4))

CELL_SIZE: Final = 20


GRID_SIZE: Final = (SCREEN_SIZE[0]//CELL_SIZE, SCREEN_SIZE[1]//CELL_SIZE)


@dataclass
class Pheromone_Grid:
    diffusion_timer: float
    decay_timer: float
    grid_list: list[int]
    len: int
    color_grid: tuple[Color, ...]

    def __init__(self):
        self.diffusion_timer = 0
        self.decay_timer = 0
        self.len = prod(GRID_SIZE)
        self.grid_list = [0] * self.len
        self.color_grid = ()
        for _ in range(self.len):
            self.color_grid += (Color(0, 120, 50),)

    def update(self, dt: float):
        self.diffusion_timer += dt
        self.decay_timer += dt

        if self.decay_timer >= DECAY_TIME:
            self.decay_timer = self.decay_timer % DECAY_TIME

            new = [min(decay(self.grid_list[i]), MAX_PER_TILE)
                   for i in range(self.len)]
            self.grid_list = new
            gen = (min(element//8, 255) for element in new)
            self.color_grid = tuple(
                Color((4*a)//5, max(120-a, 0), 50+(4*a)//5) for a in gen
            )

        if self.diffusion_timer >= DIFFUSION_TIME:

            self.diffusion_timer = self.diffusion_timer % DIFFUSION_TIME
            grid_tuple = tuple(self.grid_list)
            self.grid_list = generate_diffused_list(
                grid_tuple, generate_diffusion_amount(grid_tuple))

            gen = (min(e//8, 255) for e in self.grid_list)
            self.color_grid = tuple(
                Color((4*a)//5, max(120-a, 0), 50+(4*a)//5) for a in gen)

    def add(self,
            position: Vector2,
            strenght: int = 300,
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
                i = x+y*(grid_size[0])
                if (self.color_grid[i] != Color(0, 120, 50)):
                    rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE,
                                       CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, self.color_grid[i], rect)

    def sum(self):
        return sum(self.grid_list)


def generate_diffusion_amount(grid_list: tuple[int, ...], grid_size: tuple[int, int] = GRID_SIZE):

    grid_diffusion_amount: tuple[int, ...] = ()

    for i in range(prod(grid_size)):
        not_top_or_bottom: bool = not (
            i < grid_size[0] or i > grid_size[0]*(grid_size[1]-2))

        not_left_or_right: bool = not (
            i % grid_size[0] == 0 or (i+1) % grid_size[0] == 0)

        grid_diffusion_amount += ((DIFFUSION_EDGE * grid_list[i])
                                  // DIFFUSION_STRENGTH_MAP[not_top_or_bottom + not_left_or_right],)

    return grid_diffusion_amount


def generate_diffused_list(grid_list: tuple[int, ...], grid_diffusion_amount: tuple[int, ...],  grid_size: tuple[int, int] = GRID_SIZE):
    new_grid_list: list[int] = []
    for i in range(prod(grid_size)):

        top: bool = i < grid_size[0]
        bottom: bool = i > grid_size[0]*(grid_size[1]-2)
        left: bool = i % grid_size[0] == 0
        right: bool = (i+1) % grid_size[0] == 0

        s: int = grid_list[i] - (4 - (top+bottom+left+right)
                                 ) * grid_diffusion_amount[i]

        if not (top):
            s += grid_diffusion_amount[i - grid_size[0]]

        if not (right):
            s += grid_diffusion_amount[i + 1]

        if not (bottom):
            s += grid_diffusion_amount[i + grid_size[0]]

        if not (left):
            s += grid_diffusion_amount[i - 1]

        new_grid_list.append(min(s, MAX_PER_TILE))

    return new_grid_list


def decay(x: int) -> int:
    y = 6
    return (x-(x >> y)-min(x & ((1 << y)-1), 3))
