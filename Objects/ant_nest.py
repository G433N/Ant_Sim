from dataclasses import dataclass
from pygame import Vector2
from ECS.entity import NOT_INIT_ENTITY
from ECS.system import Command
from Objects.Componets.world_object import WorldObject
from Objects.ant import Ant
from util import random_vector


@dataclass
class AntNest(WorldObject):
    timer: float
    time: float
    spawmed: int
    spawn: int

    def __init__(self, position: Vector2):
        self.id = NOT_INIT_ENTITY
        self.position = position
        self.radius = 25
        self.color = "black"
        self.timer = 0
        self.time = 1
        self.spawmed = 0
        self.spawn = 100


def ant_nest_system(world_size: Vector2, obj: AntNest, dt: float):
    c = Command()
    obj.timer += dt
    if obj.spawmed < obj.spawn and obj.timer > obj.time:
        c.spawn(
            Ant(obj.position.copy(), random_vector(world_size)))
        obj.timer = obj.timer % obj.time
        obj.spawmed += 1
        return c
