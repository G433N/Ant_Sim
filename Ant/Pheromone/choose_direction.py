from typing import Protocol

from pygame import Vector2


class Choose_Direction(Protocol):

    def __call__(self, direction: Vector2, position: Vector2) -> Vector2:
        ...
