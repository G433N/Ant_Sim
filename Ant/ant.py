
from typing import Protocol

from pygame import Surface, Vector2

from Util.movement import Movement


class Ant(Movement, Protocol):
    position: list[Vector2]
    velocity: list[Vector2]
    acceleration: list[Vector2]

    def update(self, dt: float):
        ...

    def draw(self, screen: Surface):
        ...
