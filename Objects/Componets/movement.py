from dataclasses import dataclass
from pygame import Vector2
from Objects.Componets.world_object import WorldObject


@dataclass
class Movement(WorldObject):
    velocity: Vector2
    acceleration: Vector2


def movement_system(obj: Movement, dt: float) -> None:
    friction(obj)
    obj.velocity += obj.acceleration * dt
    obj.position += obj.velocity * dt
    obj.acceleration *= 0


def friction(obj: Movement) -> None:
    if obj.velocity.length_squared() < 1:
        return

    direction = obj.velocity.normalize()
    force = obj.velocity.length_squared() * 0.0002  # my:  fricton cof
    friction = -direction * force
    obj.velocity += friction
