from dataclasses import dataclass
from math import prod

from typing import Callable, Final

from pygame import Color, Surface, Vector2
import pygame
from Util.globals import SCREEN_SIZE

COLORS = 50

DIFFUSION_TIME: Final = 0.05
DECAY_TIME: Final = 1

DIFFUSION_EDGE: Final = 1
DIFFUSION_MIDDLE: Final = 50
MAX_PER_TILE: Final = 2047


def DIFFUSION_STRENGTH_SUM(edge: int):
    return edge * DIFFUSION_EDGE + DIFFUSION_MIDDLE


DIFFUSION_STRENGTH_MAP: Final = (DIFFUSION_STRENGTH_SUM(
    2), DIFFUSION_STRENGTH_SUM(3), DIFFUSION_STRENGTH_SUM(4))

CELL_SIZE: Final = 10


GRID_SIZE: Final = (SCREEN_SIZE[0]//CELL_SIZE, SCREEN_SIZE[1]//CELL_SIZE)


def top(i: int):
    return i > GRID_SIZE[0]*(GRID_SIZE[1]-2)


def bottom(i: int):
    return i < GRID_SIZE[0]


def left(i: int):
    return i % GRID_SIZE[0] == 0


def right(i: int):
    return (i+1) % GRID_SIZE[0] == 0


BORDER_GRID = tuple(
    (not top(i)) << 3 |
    (not bottom(i)) << 2 |
    (not left(i)) << 1 |
    (not right(i)) for i in range(prod(GRID_SIZE))
)

NOT_TOP = 1 << 3
NOT_BOTTOM = 1 << 2
NOT_LEFT = 1 << 0
NOT_RIGHT = 0


@dataclass(slots=True)
class Pheromone_Grid:
    diffusion_timer: float
    decay_timer: float
    grid_list: list[int]
    len: int
    color_grid: list[int]
    color_scale: list[int]
    sprites: list[Surface]

    def __init__(self):
        self.diffusion_timer = 0
        self.decay_timer = 0
        self.len = prod(GRID_SIZE)
        self.grid_list = [0] * self.len
        self.color_grid = [0] * self.len
        color_map: Callable[[int], int] = lambda a: (MAX_PER_TILE * a)//COLORS

        self.color_scale = [color_map(a) for a in range(COLORS+1)]

        self.sprites = [Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                        for _ in range(COLORS+1)]

        for color, surface in zip(get_colors(self.color_scale), self.sprites):
            pygame.draw.rect(surface, color, (0, 0, CELL_SIZE, CELL_SIZE))
        print(self.color_scale, len(self.sprites))
        print(self.sprites)

    def update(self, dt: float):
        self.diffusion_timer += dt
        self.decay_timer += dt

        if self.decay_timer >= DECAY_TIME:
            self.decay_timer = self.decay_timer % DECAY_TIME

            new = [min(decay(self.grid_list[i]), MAX_PER_TILE)
                   for i in range(self.len)]
            self.grid_list = new

            self.color_grid = get_color_scale(self.grid_list, self.color_scale)

        if self.diffusion_timer >= DIFFUSION_TIME:
            self.diffusion_timer = self.diffusion_timer % DIFFUSION_TIME
            self.grid_list = generate_diffused_list(
                self.grid_list, generate_diffusion_amount(self.grid_list))

            self.color_grid = get_color_scale(self.grid_list, self.color_scale)

    def add(self,
            position: Vector2,
            strength: int = 300,
            grid_size: tuple[int, int] = GRID_SIZE,
            cell_size: int = CELL_SIZE
            ):
        x = int(position.x/cell_size)
        y = int(grid_size[0]*int(position.y/cell_size))
        index = x + y
        if 0 > index or self.len <= index:
            return
        self.grid_list[index] += strength

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
                if (self.color_grid[i] != 0):
                    screen.blit(
                        self.sprites[self.color_grid[i]], (x * CELL_SIZE, y * CELL_SIZE))

    def sum(self):
        return sum(self.grid_list)


def not_top_or_bottom(i: int):
    return not bottom(i) or top(i)


def not_left_or_right(i: int):
    return not left(i) or right(i)


def generate_diffusion_amount(grid_list: list[int]):

    gen = (
        (DIFFUSION_EDGE * value) //
        DIFFUSION_STRENGTH_MAP[
            (NOT_TOP | NOT_BOTTOM) & border != 0
            +
            (NOT_LEFT | NOT_RIGHT) & border != 0]
        for value, border in zip(grid_list, BORDER_GRID))

    return tuple(gen)


def generate_diffused_list(grid_list: list[int], grid_diffusion_amount: tuple[int, ...]):
    new_grid_list: list[int] = list()

    for i in range(prod(GRID_SIZE)):

        s = ~BORDER_GRID[i]
        t, b, l, r = (s >> 3) & 1, (s >> 2) & 1, (s >> 1) & 1, s & 1

        s: int = grid_list[i] - (4 - (t+b+l+r)
                                 ) * grid_diffusion_amount[i]

        if not (t):
            s += grid_diffusion_amount[i + GRID_SIZE[0]]

        if not (r):
            s += grid_diffusion_amount[i + 1]

        if not (b):
            s += grid_diffusion_amount[i - GRID_SIZE[0]]

        if not (l):
            s += grid_diffusion_amount[i - 1]
        s = min(s, MAX_PER_TILE)
        new_grid_list.append(s)

    return new_grid_list


def get_colors(grid_list: list[int]):
    l: list[Color] = list()
    for e in grid_list:
        a = min(e//8, 255)
        b = (4*a)//5
        l.append(
            Color(b, max(120-a, 0), 50+b)
        )

    return l


def get_color_scale(grid_list: list[int], color_scale: list[int]):

    color_result: list[int] = list()
    for v in grid_list:
        for i, s in enumerate(color_scale):
            if v <= s:
                color_result.append(i)
                break
        else:
            raise ValueError("Out of bound colors")
    return color_result


def decay(x: int) -> int:
    y = 6
    return (x-(x >> y)-min(x & ((1 << y)-1), 3))
