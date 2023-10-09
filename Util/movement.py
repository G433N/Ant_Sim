
from typing import Final, Protocol

from pygame import Vector2


MY: Final = 0.0002


class Movement(Protocol):
    position: list[Vector2]
    velocity: list[Vector2]
    acceleration: list[Vector2]

    def movment_bundle(self):
        return (self.position, self.velocity, self.acceleration)


def apply_movement_physics(position: Vector2, velocity: Vector2, acceleration: Vector2, dt: float):
    apply_friction(position, velocity)
    velocity += acceleration * dt
    position += velocity * dt
    acceleration *= 0


def apply_friction(position: Vector2, velocity: Vector2):
    if velocity.length_squared() < 1:
        return

    direction = velocity.normalize()
    force = velocity.length_squared() * MY  # my:  fricton cof
    friction = -direction * force
    velocity += friction
