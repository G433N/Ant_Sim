from dataclasses import dataclass

from math import prod
from typing import Any, Final, Generator

#from Ant.Pheromone.pheromone_grid import  GRID_SIZE

GRID_SIZE = (16*4,9*4)

CHUNK_SIZE: Final = 4

CHUNK_GRID_SIZE: Final = (GRID_SIZE[0]//CHUNK_SIZE, GRID_SIZE[1]//CHUNK_SIZE)
CHUNK_GRID_LEN: Final = prod(CHUNK_GRID_SIZE)


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
        chunk_index: int,
        chunk_indexes:tuple[int,...] = CHUNK_INDEX_TUPLE,
        chunk_size: int = CHUNK_SIZE,
        grid_size: tuple[int, int] = GRID_SIZE
) -> Generator[int, Any, None]:

    chunk_start_index: int = chunk_indexes[chunk_index]
    for i in range(chunk_size**2):
        yield chunk_start_index + i % chunk_size + grid_size[0]*(i//chunk_size)


def generate_hex_map_cases(
        chunk_grid_size: tuple[int, int] = CHUNK_GRID_SIZE,
        grid_size: tuple[int, int] = GRID_SIZE
):

    hex_map: int = 0
    for i in range(prod(chunk_grid_size)):
        not_top: bool = i >= chunk_grid_size[0]
        not_bottom: bool = i <= chunk_grid_size[0]*(chunk_grid_size[1]-1)
        not_left: bool = i % chunk_grid_size[0] != 0
        not_right: bool = (i+1) % chunk_grid_size[0] != 0

        hex: int = not_top << 3 | not_bottom << 2 | not_left << 1 | not_right

        hex_map |= hex << (i << 2)
    return hex_map


HEX_MAP_CASES: int = generate_hex_map_cases()


@dataclass
class Chunk_Grid:
    """Chunking system built from a large bitmap"""
    bit_map: int

    def __init__(self):
        self.bit_map = 0

    def add(self, index: int):
        """adding the chunk on that index to the active chunks"""
        self.bit_map |= (1 << (index << 1))

        self.turn_on_lazy_around_index(index)

    def flip(self, index:int):
        """flipping the chunk on that index from active to inactive or vise versa """
        self.bit_map ^= (1 << (index << 1))

        self.uppdate_lazy_around_index(index)

    def remove(self, index:int):
        """removing the chunk on that index from the active chunks"""
        self.bit_map ^= (self.bit_map & (1 << (index << 1)))

        self.uppdate_lazy_around_index(index)

    def any_neighbour_active(
        
            self,
            index: int,
            chunk_grid_len: int = CHUNK_GRID_LEN
    ) -> bool:
        """
        Checking if any of the neighbouring chunks is active and also if the index is out of bounds
        """
        return bool(
            0 <= index
            and index < chunk_grid_len
            and (self.bit_map & (neighbour_indexes(index, 0))))

    def uppdate_lazy_around_index(
            self,
            index: int,
            chunk_grid_size: tuple[int, int] = CHUNK_GRID_SIZE
    ) -> None:
        """
        Uppdates neighbouring chunks to check if they should be lazy loaded or inactive
        """


        # index for chunk above (index)
        top_index = index - chunk_grid_size[0]
        # index for chunk bellow (index)
        bottom_index = index + chunk_grid_size[0]
        # index for chunk to the left of (index)
        left_index = index-1
        # index for chunk to the right of (index)
        right_index = index+1

        top = (
            # bool if there is a chunk active around the chunk above
            self.any_neighbour_active(top_index)
            # shifting the bool to the top index
            << 1+(
                max(0,top_index)<< 1
            )
        )

        bottom = (
            # bool if there is a chunk active around the chunk bellow
            self.any_neighbour_active(bottom_index)
            # shifting the bool to the bottom index
            << 1+(
                bottom_index<< 1
            )
        )

        left = (
            # bool if there is a chunk active around the chunk to the left
            self.any_neighbour_active(left_index)
            # shifting the bool to the left index
            << 1+(
                max(0,left_index)<< 1
            )
        )

        right = (
            # bool if there is a chunk active around the chunk to the right
            self.any_neighbour_active(right_index)
            # shifting the bool to the right index
            << 1+(
                right_index<< 1
            )
        )

        middle = (
            # bool if there is a chunk active around the chunk
            self.any_neighbour_active(index)
            # shifting the bool to the index
            << 1+(
                index<< 1
            )
        )

        self.bit_map ^= (
            self.bit_map & neighbour_indexes(index, 1)) ^ (
            top | bottom | left | right | middle)

    def turn_on_lazy_around_index(
            self,
            index: int
    ):
        """
        Forces neighbouring chunks to be lazy loaded
        """
        self.bit_map |= neighbour_indexes(index, 1)

    def __str__(
            self,
            chunk_grid_len:int = CHUNK_GRID_LEN,
            chunk_grid_size: tuple[int,int] = CHUNK_GRID_SIZE
            ):
        
        s = ""
        for i in range(chunk_grid_len):
            x = 3&(self.bit_map >>(i<<1))
            b = (chunk_grid_size[0]-i-1) % chunk_grid_size[0] == 0
            s += f"{x: <7}" + 2 * "\n" * b
        return s

def neighbour_indexes(
        chunk_index: int,
        intra_chunk_offset: int,  # offset for lazy or active
        chunk_grid_size: tuple[int, int] = CHUNK_GRID_SIZE,
        hex_map: int = HEX_MAP_CASES,
) -> int:
    """
    generates a smaller bitmap of the neighbouring chunks 
    scaled to be used seamlesly with the large bit map in the chunk class
    """

    top = (
        # bool if there is a chunk above
        (1 & (hex_map >> ((chunk_index << 2)+3)))
        << intra_chunk_offset + (
            # index for chunk above (index)
            (max(0, chunk_index - chunk_grid_size[0]))
            << 1
        )
    )

    bottom = (
        # bool if there is a chunk bellow
        (1 & (hex_map >> ((chunk_index << 2)+2)))
        << intra_chunk_offset + (
            # index for chunk bellow (index)
            (chunk_index + chunk_grid_size[0])
            << 1
        )
    )

    left = (
        # bool if there is a chunk to the left
        (1 & (hex_map >> ((chunk_index << 2)+1)))
        << intra_chunk_offset + (
            # index for chunk to the left of (index)
            (max(0, chunk_index - 1))
            << 1
        )
    )

    right = (
        # bool if there is a chunk to the right
        (1 & (hex_map >> ((chunk_index << 2))))
        << intra_chunk_offset + (
            # index for chunk to the right of (index)
            (chunk_index + 1)
            << 1
        )
    )

    middle = (
        # bool if there is a chunk at the start index (which it better be)
        1
        << intra_chunk_offset + (
            # index for chunk
            chunk_index
            << 1
        )
    )

    # returns a bitmap of all neighbouring chunks scaled to be seamless with the larger bitmap of all the chunks
    return top | bottom | left | right | middle


