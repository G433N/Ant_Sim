
from typing import Any, Final
import numpy as np
from pygame import Vector2

#from Ant.Pheromone.pheromone_grid import CELL_SIZE
CELL_SIZE: Final = 2

RADIUS = 10
CELL_RADIUS: Final = RADIUS// CELL_SIZE
ROOT_TWO: Final = np.sqrt(2)


def get_vision_area_offset(norm_dir:Vector2):
    """hehe good luck understanding this shit :O"""
    r = CELL_RADIUS//2
    return (
        np.fmin(
        np.fmax(
            np.rint(norm_dir * ROOT_TWO * r,out=np.empty(2,dtype=np.int64),casting="safe")   ,   -r)
        ,
        r
        ) 

        - (r,r)
    )

v = 3*Vector2(RADIUS,RADIUS)//2
d = Vector2(20,20)

ARRAY = np.full((CELL_RADIUS*3,CELL_RADIUS*3), 0, dtype=int)
m = get_vision_area_offset(d.normalize())+(int(v.x/CELL_SIZE),int(v.y/CELL_SIZE))

def sum_vision_field(vision_area: np.ndarray[int, np.dtype[Any]]) -> int:
    return np.sum(
            ARRAY[
                vision_area[1]:vision_area[1]+CELL_RADIUS, 
                vision_area[0]:vision_area[0]+CELL_RADIUS
                ] 
            ) 
        


ARRAY[int(v.x//CELL_SIZE)][int(v.y//CELL_SIZE)] = 2
s = sum_vision_field(m)
print(ARRAY,s)



    
