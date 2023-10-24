from __future__ import annotations
from dataclasses import dataclass
from math import cos, prod, pi, sin
import random
from typing import Any, Callable, Final

from Ant.Pheromone.add_pheromone import Add_Pheromone
from Ant.Pheromone.choose_direction import Choose_Direction

try:
    import numpy as np
    import pygame.surfarray as surfarray
except ImportError:
    raise ImportError("NumPy and Surfarray are required.")

from pygame import Surface, Vector2
from Util.globals import SCREEN_SIZE


###############################################################
# Grid constants
MAX_PER_TILE: Final = 8000
COLOR_SCALING: Final = MAX_PER_TILE//256

CELL_SIZE: Final = 2

GRID_SIZE: Final = (SCREEN_SIZE[0]//CELL_SIZE, SCREEN_SIZE[1]//CELL_SIZE)

###############################################################

###############################################################
# decay and diffusion

DIFFUSION_TIME: Final = .2
DECAY_TIME: Final = .4

CONSTANT_DECAY: Final = 7
FAST_DECAY_THRESHOLD: Final = 9
DECAY_SCALING_STRENGTH: Final = 5

# Higher values gives less amount diffused.
# Lower strength than 8 makes the diffusing cell
# no longer keep the majority of its original value.
# Lower than 4 gives negative values which is bad.
DIFFUSION_STRENGTH: Final = 30

DEFAULT_PHEROMONE_STRENGTH: Final = (MAX_PER_TILE//(CELL_SIZE**2))//2

###############################################################


###############################################################
# Ant vision

RADIUS = 10
CELL_RADIUS: Final = RADIUS // CELL_SIZE
ROOT_TWO: Final = np.sqrt(2)
FOV: Final = pi * 3

ROTATION_LEFT_30: Final = Vector2(cos(FOV/2), sin(FOV/2))
ROTATION_LEFT_15: Final = Vector2(cos(FOV/4), sin(FOV/4))
ROTATION_RIGHT_30: Final = Vector2(cos(FOV/2), -sin(FOV/2))
ROTATION_RIGHT_15: Final = Vector2(cos(FOV/4), -sin(FOV/4))

# higher value gives a smaller weight for the two in between directions
IN_BETWEEN_DIRECTION_WEIGHT_SCALING: Final = 5

# higher value gives a smaller base weight for the forward direction
FORWARD_BASE_WEIGHT_SCALING: Final = 20

###############################################################


class PheromoneHandler:

    pheromones: dict[str, Pheromone_Grid]

    def __init__(self, pheromones: dict[str, Pheromone_Grid]) -> None:
        self.pheromones = pheromones
        self._data = pheromones.values()

    def update(self, dt: float):
        for pheromone in self._data:
            pheromone.update(dt)

    def add_functions(self) -> dict[str, Add_Pheromone]:
        return {k: v.add for k, v in self.pheromones.items()}

    def direction_functions(self) -> dict[str, Choose_Direction]:
        return {k: v.get_new_direction for k, v in self.pheromones.items()}

    def draw(self, surface: Surface):
        array = surfarray.pixels3d(surface)  # type: ignore
        r = np.zeros(GRID_SIZE, np.int32)
        g = np.zeros(GRID_SIZE, np.int32)
        b = np.zeros(GRID_SIZE, np.int32)
        l = len(self._data)

        for pheromone in self._data:
            _r, _g, _b = pheromone.shader()
            r += _r
            g += _g
            b += _b

        r //= l
        g //= l
        b //= l

        for x in range(CELL_SIZE):
            for y in range(CELL_SIZE):
                array[y::CELL_SIZE, x::CELL_SIZE, 0] = r
                array[y::CELL_SIZE, x::CELL_SIZE, 1] = g
                array[y::CELL_SIZE, x::CELL_SIZE, 2] = b


@dataclass(slots=True)
class Pheromone_Grid:
    diffusion_timer: float
    decay_timer: float
    len: int
    grid_array: np.ndarray[int, np.dtype[np.int32]]
    surface: Surface
    # TODO : Add color map function and add as functions so that we can have different for different pheromones

    def __init__(self):
        self.diffusion_timer = 0
        self.decay_timer = 0
        self.len = prod(GRID_SIZE)
        self.surface = Surface(SCREEN_SIZE)
        self.grid_array = np.zeros(GRID_SIZE, np.int32)

    def update(self, dt: float):
        self.diffusion_timer += dt
        self.decay_timer += dt

        if self.decay_timer >= DECAY_TIME:
            self.decay_timer %= DECAY_TIME
            self.grid_array = decay(self.grid_array)

        if self.diffusion_timer >= DIFFUSION_TIME:
            self.diffusion_timer %= DIFFUSION_TIME
            self.grid_array = np.fmin(
                diffused_array(self.grid_array), MAX_PER_TILE)

    def add(self,
            position: Vector2,
            strength: int = DEFAULT_PHEROMONE_STRENGTH,
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

    def shader(self):

        a = np.fmin(self.grid_array//COLOR_SCALING, 255)
        c = (4*a)//5
        r = c
        g = np.fmax(120-a, 0)
        b = 50 + c
        return r, g, b

    def sum(self):
        return sum(self.grid_array)

    def get_new_direction(
            self,
            direction: Vector2,
            position: Vector2,
            grid_size: tuple[int, int] = GRID_SIZE,
            cell_size: int = CELL_SIZE
    ) -> Vector2:
        """
        takes in a direction in the form of a normalized vector and
        a position vector,
        then based on the pheromones on the grid
        returns a new direction vector 
        """

        x = int(position.x/cell_size)
        y = int(position.y/cell_size)
        if (
            CELL_RADIUS > x or
            CELL_RADIUS > y or
            grid_size[0]-CELL_RADIUS <= x or
            grid_size[1]-CELL_RADIUS <= y
        ):
            return direction
        left: Vector2 = \
            rotate_normal(direction, ROTATION_LEFT_30)
        right: Vector2 = \
            rotate_normal(direction, ROTATION_RIGHT_30)

        left_weight: np.int32 = \
            self.get_pheromone_amount(left, (x, y))

        forward_weight: np.int32 = (
            self.get_pheromone_amount(direction, (x, y)) +
            (MAX_PER_TILE*CELL_RADIUS**2)//FORWARD_BASE_WEIGHT_SCALING
        )

        right_weight: np.int32 = \
            self.get_pheromone_amount(right, (x, y))

        directions_weights: tuple[np.int32, ...] = (
            left_weight,
            (left_weight+forward_weight)//IN_BETWEEN_DIRECTION_WEIGHT_SCALING,
            forward_weight,
            (right_weight+forward_weight)//IN_BETWEEN_DIRECTION_WEIGHT_SCALING,
            right_weight
        )

        picked_direction = choose_value(int(np.sum(directions_weights)))

        i = 0
        for j in directions_weights:
            if picked_direction <= j:
                break
            picked_direction -= j
            i += 1

        match i:
            case 0:
                return left
            case 1:
                return rotate_normal(direction, ROTATION_LEFT_15)
            case 2:
                return direction
            case 3:
                return rotate_normal(direction, ROTATION_RIGHT_15)
            case 4:
                return right
            case _:
                raise ValueError(
                    "something wrong with that loop or chosen direction")

    def sum_vision_field(self, first_index: np.ndarray[int, np.dtype[Any]], size: int = CELL_RADIUS) -> np.int32:
        """returns the sum of pheromones in a given area"""
        return np.sum(
            self.grid_array[
                first_index[1]:first_index[1]+size,
                first_index[0]:first_index[0]+size
            ]
        )

    def get_pheromone_amount(self, direction: Vector2, pos: tuple[int, int]):
        """returns the sum of pheromones in a given direction"""
        return \
            self.sum_vision_field(
                get_vision_field_offset(direction)+pos
            )


def choose_value(end: int, start: int = 0):
    return random.randrange(start, end+1)


def decay(
    x: np.ndarray[int, np.dtype[np.int32]]
) -> np.ndarray[int, np.dtype[np.int32]]:
    """Element wise decay on numpy array"""
    return (
        # for each element in the given array returns the value of that element
        #  subtracted by a calculated decay amount
        x

        # bit shifting x by the scaling factor for a faster floor function
        # then scaling up the result by the scaling strength to make the result have more impact
        # in short this part makes larger numbers decay faster
        # the threshold creates a threshold for what size it works on
        # the strength shifts the strength of the decay
        - ((x >> FAST_DECAY_THRESHOLD) << DECAY_SCALING_STRENGTH)

        # this part is for handling a more constant decay
        # which then disappears when the given elements value is 0

        # using constant_decay for a constant decay
        # unless the constant is larger than the value of the given element then decay by that value
        - np.fmin(CONSTANT_DECAY, x)
    )


def diffusion(arr: np.ndarray[int, np.dtype[np.int32]]):
    """
    Takes in a 2D-array and treats each element as a cell in a 2D-grid.
    It returns a new 2D-array where each cell has given its value to all neighboring cells 
    and also subtracted away how many copies of itself each cell has given to its neighbors
    """
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
    """
    takes in an array and returns a copy of that array but
    with a second copy of the first row on top 
    and a second copy of the bottom row at the bottom
    """
    return np.vstack((arr[0], arr, arr[-1]))


def diffused_array(arr: np.ndarray[int, np.dtype[np.int32]]):
    """
    takes in a 2D-array and treats each element as a cell in a 2D-grid
    It returns a new 2D-array where each cell has diffused into its neighbors
    """
    return arr + diffusion(arr//DIFFUSION_STRENGTH)


def get_vision_field_offset(norm_dir: Vector2, half_size: int = CELL_RADIUS//2):
    """
    Takes in a normalized vector as direction and optionally a size 
    then returns the top left index of a square which the direction vector is pointing at.
    The square is adjacent to the origin (0,0) and has a side length equal to the size
    """
    return (
        np.fmin(

            np.fmax(
                # scales the normalized vector
                #  then element wise rounds to the nearest integer
                np.rint(norm_dir * ROOT_TWO * half_size,
                        out=np.empty(2, dtype=int),
                        casting="unsafe"
                        ),
                -half_size
            ),
            half_size
        )
        # offset to get the index in the top left and not in the middle of the vision field
        - (half_size, half_size)
    )


def rotate_normal(norm_dir: Vector2, rotation_vector: Vector2):
    """rotates the first vector by the second (both needs to be normalized)"""
    return Vector2(
        norm_dir.x * rotation_vector.x - norm_dir.y * rotation_vector.y,
        norm_dir.y * rotation_vector.x + norm_dir.x * rotation_vector.y
    )
