from dataclasses import dataclass

from math import prod
from typing import Any, Final, Generator

from Ant.Pheromone.pheromone_grid import GRID_SIZE

CHUNK_SIZE: Final = 4

CHUNK_GRID_SIZE: Final = (GRID_SIZE[0]//CHUNK_SIZE, GRID_SIZE[1]//CHUNK_SIZE)


def generate_chunk_index_tuple(
        chunk_grid_size:    tuple[int, int] = CHUNK_GRID_SIZE,
        grid_size:          tuple[int, int] = GRID_SIZE
) -> tuple[int, ...]:

    sub_grid_index_list: tuple[int, ...] = ()
    for i in range(prod(chunk_grid_size)):
        sub_grid_index_list += (
            4*((i % chunk_grid_size[0]) + grid_size[0]*(i//chunk_grid_size[0])),)
    return sub_grid_index_list


CHUNK_INDEX_TUPLE: Final = generate_chunk_index_tuple()


def get_grid_indexes_from_chunk(
        chunk_start_index: int,
        chunk_size: int = CHUNK_SIZE,
        grid_size: tuple[int, int] = GRID_SIZE
) -> Generator[int, Any, None]:

    for i in range(chunk_size**2):
        yield chunk_start_index + i % chunk_size + grid_size[0]*(i//chunk_size)


def generate_hex_map_cases(
        chunk_grid_size: tuple[int, int] = CHUNK_GRID_SIZE,
        grid_size: tuple[int, int] = GRID_SIZE
):

    hex_map: int = 0
    for i in range(prod(chunk_grid_size)):
        not_top: bool = i >= grid_size[0]
        not_bottom: bool = i <= grid_size[0]*(grid_size[1]-2)
        not_left: bool = i % grid_size[0] != 0
        not_right: bool = (i+1) % grid_size[0] != 0

        hex: int = not_top << 3 | not_bottom << 2 | not_left << 1 | not_right

        hex_map |= hex << (i << 2)
    return hex_map


HEX_MAP_CASES: int = generate_hex_map_cases()


@dataclass
class Chunk_Grid:
    bit_map: int

    def __init__(self):
        self.bit_map = 0

    def add(self, index: int):
        self.bit_map |= index_to_active(index)

        self.turn_on_lazy_around_index(index)

    def any_neighbour_active(
            self,
            index: int,
    ):

        return bool(self.bit_map & (neighbour_indexes(index,0)))

    def uppdate_lazy_around_index(
            self,
            index: int
    ):

        top = self.any_neighbour_active(top_(index)) << 1+(top_(index) << 1)
        bottom = self.any_neighbour_active(
            bottom_(index)) << 1+(bottom_(index) << 1)
        left = self.any_neighbour_active(left_(index)) << 1+(left_(index) << 1)
        right = self.any_neighbour_active(
            right_(index)) << 1+(right_(index) << 1)
        middle = self.any_neighbour_active(index) << 1+(index << 1)

        self.bit_map ^= (self.bit_map & neighbour_indexes(index,1)) ^ (
            top | bottom | left | right | middle)

    def turn_on_lazy_around_index(
            self,
            index: int
    ):

        self.bit_map |= neighbour_indexes(index,1)


def neighbour_indexes(
        index: int,
        offset: int, #offset for lazy or active
        chunk_grid_size: tuple[int, int] = CHUNK_GRID_SIZE,
):

    top = (
        get_hex_from_map(index, 3) #bool if there is a chunk above
        << offset + ( 
            (max(0, index - chunk_grid_size[0])) #index for chunk above (index)
            << 1
        )
    )

    bottom = (
        get_hex_from_map(index, 2) #bool if there is a chunk bellow
        << offset + (
            (index + chunk_grid_size[0]) #index for chunk bellow (index)
            << 1
        )
    )

    left = (
        get_hex_from_map(index, 1) #bool if there is a chunk to the left
        << offset + (
            (max(0, index - 1)) #index for chunk to the left of (index)
            << 1
        )
    )

    right = (
        get_hex_from_map(index, 0) #bool if there is a chunk to the right
        << offset + (
            (index + 1) #index for chunk to the right of (index)
            << 1
        )
    )

    middle = (
        1
        << offset + (
            (index)
            << 1
        )
    )

    return top | bottom | left | right | middle


def top_(
        index: int,
        chunk_grid_size: tuple[int, int] = CHUNK_GRID_SIZE
) -> int:
    return max(0, index - chunk_grid_size[0])


def bottom_(
        index: int,
        chunk_grid_size: tuple[int, int] = CHUNK_GRID_SIZE
) -> int:
    return index + chunk_grid_size[0]


def left_(
        index: int
) -> int:
    return max(0, index - 1)


def right_(
        index: int
) -> int:
    return index + 1


def get_hex_from_map(
        index: int,
        offset: int = 0,
        hex_map: int = HEX_MAP_CASES):

    return 1 & (hex_map >> (index << 2 + offset))


def index_to_active(index: int):
    return 1 << (index << 1)


def index_to_lazy(index: int):
    return 1 << 1+(index << 1)
