from dataclasses import dataclass

from math import prod
from typing import Any, Final, Generator

from Ant.Pheromone.pheromone_grid import GRID_SIZE


CHUNK_SIZE: Final = 4

CHUNK_GRID_SIZE: Final = (GRID_SIZE[0]//CHUNK_SIZE, GRID_SIZE[1]//CHUNK_SIZE)

def generate_chunk_index_tuple(
        chunk_grid_size:    tuple[int,int] = CHUNK_GRID_SIZE,
        grid_size:          tuple[int,int] = GRID_SIZE
        ) ->                tuple[int, ...]:
    
    sub_grid_index_list: tuple[int,...] = ()
    for i in range(prod(chunk_grid_size)):
        sub_grid_index_list += (4*( (i%chunk_grid_size[0])+grid_size[0]*(i//chunk_grid_size[0]) ),)
    return sub_grid_index_list

CHUNK_INDEX_TUPLE: Final = generate_chunk_index_tuple()

def get_grid_index_from_chunk(
        chunk_start_index: int,
        chunk_size: int = CHUNK_SIZE,
        grid_size: tuple[int,int] = GRID_SIZE
        ) -> Generator[int, Any, None]:
    
    for i in range(chunk_size**2):
        yield chunk_start_index + i%chunk_size + grid_size[0]*(i//chunk_size)

def generate_hex_map_cases(index: int , grid_size: tuple[int,int] = GRID_SIZE):
    top: bool = index < grid_size[0]
    bottom: bool = index > grid_size[0]*(grid_size[1]-2)
    left: bool = index % grid_size[0] == 0
    right: bool = (index+1) % grid_size[0] == 0


@dataclass
class Chunk_Grid:
    bit_map: int

    def __init__(self):
        self.bit_map = 0

    def add(self,index:int):
        self.bit_map |= index_active(index)

        self.uppdate_lazy(index)
    
    
    
    

    def uppdate_lazy(
            self,
            index:int,
            chunk_grid_size: tuple[int,int] = CHUNK_GRID_SIZE
            ):
        self.bit_map |= (()|()|()|()|)
        

def index_active(index:int):
        return 1<<(index<<1)


def index_lazy(index:int):
    return 1<<1+(index<<1)

