from typing import Final
from pygame import Surface, Vector2, draw
from Ant.Pheromone.add_pheromone import add_pheromone
from Ant.ant import Ant
from Util.movement import apply_movement_physics
from Util.util import random_vector

ANT_ACCELERATION: Final = 300
ANT_COLOR: Final = "black"
ANT_RADIUS: Final = 5

PHEROMONE_DELAY: Final = .5

TARGET_COLOR: Final = "blue"
TARGET_RADIUS: Final = 2


class SimpleAnts(Ant):
    position: list[Vector2]
    velocity: list[Vector2]
    acceleration: list[Vector2]
    timer: list[float]
    target: list[Vector2]
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

    def add(self, position: Vector2, spawn_area: Vector2):
        self.position.append(position)
        self.velocity.append(Vector2())
        self.acceleration.append(Vector2())
        self.timer.append(0)
        self.target.append(random_vector(spawn_area))

    def update(self, dt: float):

        for i, (position, velocity, acceleration, target) in enumerate(zip(*self.movment_bundle(), self.target)):
            basic_ant_movement(position, velocity, acceleration,
                               target, dt, self.world_size)

            self.timer[i] += dt
            time = self.timer[i]
            if time >= PHEROMONE_DELAY:
                self.timer[i] = time % PHEROMONE_DELAY
                self.spawn_pheromone(position.copy())

    def draw(self, screen: Surface):
        for position, target, velocity in zip(self.position, self.target, self.velocity):
            draw.circle(screen, ANT_COLOR, position, ANT_RADIUS)
            draw.circle(screen, TARGET_COLOR, target, TARGET_RADIUS)
            if velocity.length_squared() < 1:
                continue
            draw.circle(screen, ANT_COLOR, position +
                        velocity.normalize() * ANT_RADIUS * 1.2, ANT_RADIUS * 0.8)


def basic_ant_movement(position: Vector2, velocity: Vector2, acceleration: Vector2, target: Vector2, dt: float, world_size: Vector2):
    apply_movement_physics(position, velocity, acceleration, dt)
    if position.distance_squared_to(target) < 10**2:
        target.xy = random_vector(world_size)

    dir = (target - position).normalize()
    acceleration += dir * ANT_ACCELERATION
