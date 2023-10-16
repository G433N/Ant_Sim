from dataclasses import dataclass
from math import prod
from typing import Callable, Final, cast
from numpy import ndarray, vectorize

try:
    import numpy as np
    import pygame.surfarray as surfarray
except ImportError:
    raise ImportError("NumPy and Surfarray are required.")

from pygame import Color, Surface, Vector2
import pygame
from Util.globals import SCREEN_SIZE

COLORS = 50  # Must divide MAX_PER_TILE

DIFFUSION_TIME: Final = 2
DECAY_TIME: Final = 4

DIFFUSION_EDGE: Final = 1
DIFFUSION_MIDDLE: Final = 5
MAX_PER_TILE: Final = 2000


CELL_SIZE: Final = 5

GRID_SIZE: Final = (SCREEN_SIZE[0]//CELL_SIZE, SCREEN_SIZE[1]//CELL_SIZE)


@dataclass(slots=True)
class Pheromone_Grid:
    diffusion_timer: float
    decay_timer: float
    len: int
    grid_array: np.ndarray[int, np.dtype[np.int32]]
    color_array: np.ndarray[int, np.dtype[np.int32]]
    surface: Surface

    def __init__(self):
        self.diffusion_timer = 0
        self.decay_timer = 0
        self.len = prod(GRID_SIZE)
        self.surface = Surface(SCREEN_SIZE)
        self.grid_array = np.zeros(GRID_SIZE, np.int32)
        array = np.expand_dims(self.grid_array, axis=2)
        array = np.repeat(array, 3, axis=2)
        array = np.repeat(array, CELL_SIZE, 0)
        array = np.repeat(array, CELL_SIZE, 1)
        self.color_array = array

    def update(self, dt: float):
        self.diffusion_timer += dt
        self.decay_timer += dt

        if self.decay_timer >= DECAY_TIME:
            self.decay_timer = self.decay_timer % DECAY_TIME
            self.grid_array = decay(self.grid_array)

        if self.diffusion_timer >= DIFFUSION_TIME:
            self.diffusion_timer = self.diffusion_timer % DIFFUSION_TIME
            self.grid_array = np.fmin(
                diffused_array(self.grid_array), MAX_PER_TILE)

    def add(self,
            position: Vector2,
            strength: int = 80,
            grid_size: tuple[int, int] = GRID_SIZE,
            cell_size: int = CELL_SIZE
            ):
        x = int(position.x/cell_size)
        y = int(position.y/cell_size)
        if 0 > x or 0 > y or grid_size[0] <= x or grid_size[1] <= y:
            return
        self.grid_array[x][y] = min(
            self.grid_array[x][y]+strength, MAX_PER_TILE)

    def __str__(self):
        return f"\n{self.grid_array}\n"

    def draw(self, grid_size: tuple[int, int] = GRID_SIZE):
        array = np.fmin(self.grid_array//8, 255)
        x = (4*array)//5
        r = x.copy()
        g = np.fmax(120-array, 0)
        b = 50 + x

        for x in range(CELL_SIZE):
            for y in range(CELL_SIZE):
                self.color_array[y::CELL_SIZE, x::CELL_SIZE, 0] = r
                self.color_array[y::CELL_SIZE, x::CELL_SIZE, 1] = g
                self.color_array[y::CELL_SIZE, x::CELL_SIZE, 2] = b

        surfarray.blit_array(
            self.surface,
            self.color_array
        )

        return self.surface

    def sum(self):
        return sum(self.grid_array)


def decay(x: np.ndarray[int, np.dtype[np.int32]]) -> np.ndarray[int, np.dtype[np.int32]]:
    y = 9
    return (x-(x >> y)-np.fmin(x & ((1 << y)-1), 3))


def diffusion(arr: np.ndarray[int, np.dtype[np.int32]]):
    vertical_arr = diffusion_stack(arr)
    horizon_arr = diffusion_stack(np.transpose(arr))
    return (
        vertical_arr[:-2]
        + vertical_arr[2:]
        + np.transpose(
            horizon_arr[:-2]
            + horizon_arr[2:]
        )
        - 4*arr
    )


def diffusion_stack(arr: np.ndarray[int, np.dtype[np.int32]]):
    return np.vstack((arr[0], arr, arr[-1]))


def diffused_array(arr: np.ndarray[int, np.dtype[np.int32]]):
    return arr + diffusion(arr//20)
