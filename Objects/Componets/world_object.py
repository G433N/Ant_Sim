from dataclasses import dataclass
from pygame import Vector2
from ECS.entity import Entity


@dataclass
class WorldObject(Entity):
    """Base class for all worldobjects and should not be instanced"""
    position: Vector2
    radius: float
    color: str
