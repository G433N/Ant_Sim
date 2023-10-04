

from dataclasses import dataclass

from pygame import Vector2

from world import WorldObject


@dataclass
class AntNest(WorldObject):
    timer: float
    time: float
    spawmed: int
    spawn: int

    def __init__(self, position: Vector2):
        self.position = position
        self.radius = 25
        self.color = "black"
        self.timer = 0
        self.time = 1
        self.spawmed = 0
        self.spawn = 100