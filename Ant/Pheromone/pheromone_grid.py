from dataclasses import dataclass
from math import prod

from typing import Final
from Util.globals import SCREEN_SIZE

TIME: Final = 1
DIFFUSION_EDGE: Final = 10
DIFFUSION_CORNER: Final = 5
DIFFUSION_MIDDLE: Final = 250
DECAY_STRENGTH: Final = 0.1
CELL_SIZE: Final = 20


BIT_MAPS: Final = (
                0b110110000, 0b111111000, 0b011011000,
                0b110110110, 0b111111111, 0b011011011,
                0b000110110, 0b000111111, 0b000011011)




def DIFFUSION_STRENGTH_SUM(corner: int, edge: int):
    return corner * DIFFUSION_CORNER + edge * DIFFUSION_EDGE + DIFFUSION_MIDDLE


GRID_SIZE: Final = (SCREEN_SIZE[0]//CELL_SIZE, SCREEN_SIZE[1]//CELL_SIZE)

def bleed_mapper(k: float,corner:int,edge:int,middle:int):
    return (k*corner,   k*edge,     k*corner,
            k*edge,     k*middle,   k*edge,
            k*corner,   k*edge,     k*corner)


DIFFUSION_BLEED_MAP: Final = bleed_mapper((1-DECAY_STRENGTH), DIFFUSION_CORNER, DIFFUSION_EDGE, DIFFUSION_MIDDLE)

DIFFUSION_STRENGTH_MAP: Final = bleed_mapper(1, DIFFUSION_STRENGTH_SUM(1,2), DIFFUSION_STRENGTH_SUM(2,3), DIFFUSION_STRENGTH_SUM(4,4))

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
            self.grid_list = get_diffused_list(self.grid_list,self.grid_size)

    def __str__(self):
        s = ""
        for i, x in enumerate(self.grid_list):
            b = (self.grid_size[0]-i-1) % self.grid_size[0] == 0
            s += f"{round(x, 3): <7}" + 2 * "\n" * b
        return s + f"\n{self.sum()}"

    def sum(self):
        return sum(self.grid_list)

def get_diffused_list(grid_list:list[float], grid_size: tuple[int,int] = GRID_SIZE):
        new_grid_list: list[float] = []
        for i in range(prod(grid_size)):
            case: int = get_map_case(i, grid_size)
            s=0
            for x,y in int_and_bin_gen(9):
                if (BIT_MAPS[case]&y):
                    s+= (DIFFUSION_BLEED_MAP[x]/
                        DIFFUSION_STRENGTH_MAP[case]*
                        grid_list[i+x % 3-1+(x//3-1)*grid_size[0]]
                    ) 
            new_grid_list.append(s)
        return new_grid_list
    
def get_map_case(index: int, grid_size: tuple[int,int] = GRID_SIZE) -> int:
        top: bool = index < grid_size[0]
        bottom: bool = index > grid_size[0]*(grid_size[1]-2)
        left: bool = index % grid_size[0] == 0
        right: bool = (index+1) % grid_size[0] == 0

        match (left,top,right,bottom):
            case True, True, False, False:
                """Top_Left"""
                return 0

            case False, True, False, False:
                """"Top_Middle"""
                return 1

            case False, True, True, False:
                """"Top_Right"""
                return 2

            case True, False, False, False:
                """"Middle_Left"""
                return 3

            case False, False, False, False:
                """"Middle_Middle"""
                return 4

            case False, False, True, False:
                """"Middle_Right"""
                return 5

            case True, False, False, True:
                """"Bottom_Left"""
                return 6

            case False, False, False, True:
                """"Bottom_Middle"""
                return 7

            case False, False, True, True:
                """"Bottom_Right"""
                return 8

            case _:
                raise ValueError



def int_and_bin_gen(n:int):
    num = 1
    for x in range(n):
        yield x,num
        num = num << 1

pg = PheromoneGrid((10, 10))
pg.grid_list[25] = 10
pg.grid_list[80] = 10
print(pg)
for _ in range(1):
    pg.update(TIME)
    print(pg)
