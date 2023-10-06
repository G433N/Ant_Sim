from typing import Protocol

from pygame import Vector2


class add_pheromone(Protocol):

    def __call__(self, position: Vector2) -> None:
        ...
