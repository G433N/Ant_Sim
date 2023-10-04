from dataclasses import dataclass
from pygame import Vector2

@dataclass
class WorldObject:
    position: Vector2
    radius: float
    color: str
