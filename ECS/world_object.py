from dataclasses import dataclass
from pygame import Vector2
from ECS.util import Entity

@dataclass
class WorldObject:
    id: Entity # Should be set to -1
    position: Vector2
    radius: float
    color: str
