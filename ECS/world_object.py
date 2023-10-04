from dataclasses import dataclass
from pygame import Vector2
from ECS.util import Entity

@dataclass
class WorldObject:
    """Base class for all worldobjects and should not be instanced"""
    id: Entity # Should be set to -1
    position: Vector2
    radius: float
    color: str
