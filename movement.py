
from typing import Final, Protocol

from data_types import Acceleration, Position, Velocity

MY: Final = 0.0002


class Movement(Protocol):
    position: list[Position]
    velocity: list[Velocity]
    acceleration: list[Acceleration]

    def get_movment_bundle(self):
        return (self.position, self.velocity, self.acceleration)


def apply_movement_physics(position: Position, velocity: Velocity, acceleration: Acceleration, dt: float):
    apply_friction(position, velocity)
    velocity += acceleration * dt
    position += velocity * dt
    acceleration *= 0


def apply_friction(position: Position, velocity: Velocity):
    if velocity.length_squared() < 1:
        return

    direction = velocity.normalize()
    force = velocity.length_squared() * MY  # my:  fricton cof
    friction = -direction * force
    velocity += friction
