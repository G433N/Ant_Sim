
from typing import Final, Protocol

from pygame import Vector2


MY: Final = 0.0002


class Movement(Protocol):
    position: list[Vector2]
    velocity: list[Vector2]
    acceleration: list[Vector2]

    def movement_bundle(self):
        return (self.position, self.velocity, self.acceleration)


def apply_movement_physics(position: Vector2, velocity: Vector2, acceleration: Vector2, dt: float):
    velocity += acceleration * dt
    position += velocity * dt
    acceleration *= 0


def get_friction(direction: Vector2, speed_squared: float):
    if not direction:
        return Vector2()
    force = speed_squared * MY  # my:  friction cof
    friction = -direction * force
    return friction
