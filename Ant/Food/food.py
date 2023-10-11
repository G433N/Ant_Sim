

from typing import Final
from pygame import Surface, Vector2, draw

from Util.chunked_data import ChunkedData
from Util.globals import WORLD_SIZE
from Util.util import random_vector_disc

"""
Note to future me
Probably useless to check if food is eaten before pathing to it
because the chance that to 2 or more ants eat the same food the same frame
is very very low

never mind u can max eat one food per ant per frame 
and an ant check every possibale food before the next ant does the same
"""
FOOD_SIZE: Final = 4


class Food:
    position: ChunkedData[Vector2]

    def __init__(self) -> None:
        self.position = ChunkedData(WORLD_SIZE)

    def add(self, position: Vector2, amount: int, radius: float):
        for _ in range(amount):
            v = position + random_vector_disc(radius)
            self.position.add(v, v)

    def draw(self, surface: Surface):
        for position in self.position.get_data():
            draw.circle(surface, "yellow", position, FOOD_SIZE)
