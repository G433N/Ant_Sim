from typing import Protocol

from pygame import Vector2


class Add_Pheromone(Protocol):

    def __call__(self, position: Vector2) -> None:
        ...
