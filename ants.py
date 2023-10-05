from typing import Final
from pygame import Surface, Vector2, draw
from add_pheromone import add_pheromone
from data_types import Acceleration, Position, Target, Velocity
from movement import Movement, apply_movement_physics
from util import random_vector

ANT_ACCELERATION: Final = 3000
ANT_COLOR: Final = "red"
ANT_RADIUS: Final = 5

PHEROMONE_DELAY: Final = 1

TARGET_COLOR: Final = "blue"
TARGET_RADIUS: Final = 2


class Ants(Movement):
    position: list[Position]
    velocity: list[Velocity]
    acceleration: list[Acceleration]
    timer: list[float]
    target: list[Position]
    world_size: Vector2
    spawn_pheromone: add_pheromone

    def __init__(self, world_size: Vector2, spawn_pheromone: add_pheromone) -> None:
        self.world_size = world_size
        self.position = list()
        self.velocity = list()
        self.timer = list()
        self.acceleration = list()
        self.target = list()
        self.spawn_pheromone = spawn_pheromone

    def add(self, position: Position, spawn_area: Position):
        self.position.append(position)
        self.velocity.append(Vector2())
        self.acceleration.append(Vector2())
        self.timer.append(0)
        self.target.append(random_vector(spawn_area))

    def update(self, dt: float):

        for i, (position, velocity, acceleration, target) in enumerate(zip(*self.get_movment_bundle(), self.target)):
            _update_ant(position, velocity, acceleration,
                        target, dt, self.world_size)

            self.timer[i] += dt
            time = self.timer[i]
            if time >= PHEROMONE_DELAY:
                self.timer[i] = time % PHEROMONE_DELAY
                self.spawn_pheromone(position.copy())

    def draw(self, screen: Surface):
        for position, target in zip(self.position, self.target):
            draw.circle(screen, ANT_COLOR, position, ANT_RADIUS)
            draw.circle(screen, TARGET_COLOR, target, TARGET_RADIUS)


def _update_ant(position: Position, velocity: Velocity, acceleration: Acceleration, target: Target, dt: float, world_size: Vector2):
    apply_movement_physics(position, velocity, acceleration, dt)
    if position.distance_squared_to(target) < 10**2:
        target.xy = random_vector(world_size)

    dir = (target - position).normalize()
    acceleration += dir * ANT_ACCELERATION * dt
