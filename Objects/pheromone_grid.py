from dataclasses import dataclass
from math import prod


@dataclass
class PhermoneGrid:
    decay_time: float
    decay_strength: float
    diffusion_time: float
    timer: float
    grid_list: list[list[float]]
    cell_size: tuple[int, int]
    grid_size: tuple[int, int]

    def __init__(self, screen_size: tuple[int, int]):
        self.decay_time = 1
        self.decay_strength = 0.1
        self.diffusion_time = 1
        self.timer = 0
        self.cell_size = (20, 20)
        self.grid_size = (
            screen_size[0]//self.cell_size[0], screen_size[1]//self.cell_size[1])
        self.grid_list = [[0]*2] * prod(self.grid_size)


def phermone_grid_system(obj: PhermoneGrid, dt: float):
    obj.timer += dt
    if obj.timer > obj.decay_time:
        obj.timer = obj.timer % obj.decay_time
        obj.grid_list = [[y*(1-obj.decay_strength) 
                         for y in x]
                         for x in obj.grid_list]

    if obj.timer > obj.diffusion_time:
        obj.timer = obj.timer % obj.diffusion_time






def get_grid_neighbours(index: int, grid_size: tuple[int,int]) -> tuple[list[int], list[int]]:
    
    not_top: bool = index >= grid_size[0]
    not_bottom: bool = index <= grid_size[0]*(grid_size[1]-1)
    not_left: bool = index%grid_size[0]!=0
    not_right: bool = (index+1)%grid_size[0]!=0
    
    neighbour_to_add: list[bool] = [
     not_left and not_top   , not_top   , not_right and not_top   ,
     not_left               , True      , not_right               ,
     not_left and not_bottom, not_bottom, not_right and not_bottom]
    
    neighbour_corners: list[int] = []
    neighbour_edges: list[int] = []
    
    for x in range(9):
        if neighbour_to_add[x]:
            if x in [0,2,6,8]:
                neighbour_corners.append(index+x%3-1+(x//3-1)*grid_size[0])
            else:
                neighbour_edges.append(index+x%3-1+(x//3-1)*grid_size[0])
    return (neighbour_corners,neighbour_edges)
