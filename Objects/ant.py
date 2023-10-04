from dataclasses import dataclass

from pygame import Vector2
from Objects.Componets.movment import Movment
from util import random_vector


@dataclass
class Ant(Movment):
    target: Vector2

    def __init__(self, positon: Vector2, target: Vector2) -> None:
        self.position = positon
        self.velocity = Vector2()
        self.acceleration = Vector2()
        self.color = "red"
        self.radius = 5
        self.target = target


def update_ant(world_size: Vector2, obj: Ant, dt: float):
    if obj.position.distance_squared_to(obj.target) < 100:
        obj.target = random_vector(world_size)

    dir = (obj.target - obj.position).normalize()
    obj.acceleration = dir * 150
