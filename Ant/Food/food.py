

from math import cos, pi, sin, sqrt
from random import random
from pygame import Surface, Vector2, draw

"""
Note to future me
Probably useless to check if food is eaten before pathing to it
because the chance that to 2 or more ants eat the same food the same frame
is very very low

never mind u can max eat one food per ant per frame 
and an ant check every possibale food before the next ant does the same
"""


class Food:
    position: list[Vector2]

    def __init__(self) -> None:
        self.position = list()
        self._eaten = list()

    def add(self, position: Vector2, amount: int, radius: float):
        for _ in range(amount):
            # https://rh8liuqy.github.io/Uniform_Disk.html
            r1, r2 = random(), random()  # Very not uniform but what ever
            v = position + Vector2(
                radius * sqrt(r2) * cos(2 * pi * r1),
                radius * sqrt(r2) * sin(2 * pi * r1)
            )
            self.position.append(v)

    def draw(self, surface: Surface):
        for position in self.position:
            draw.circle(surface, "yellow", position, 4)
