from enum import Enum, auto
from math import sqrt
from random import random
from typing import Final
from pygame import Surface, Vector2, draw
from Ant.Food.food import Food
from Ant.Pheromone.add_pheromone import add_pheromone
from Ant.ant import Ant
from Util.chunked_data import ChunkedData
from Util.globals import WORLD_SIZE
from Util.util import bounds, random_normal_vector
import numpy as np

ANT_ACCELERATION: Final = 20
ANT_COLOR: Final = "black"
ANT_RADIUS: Final = 3

PHEROMONE_DELAY: Final = 1
MY: Final = 0.0002

WANDER_DELAY: Final = 3

TARGET_COLOR: Final = "blue"
TARGET_RADIUS: Final = 2

VISION_RANGE: Final = 25

SIZE = 8

"""
TODO
Random ant movement offset
Search for food
Return home with food
Switch phermone type and internal state
follow phermone
"""


class AntState(Enum):
    Searching = auto(),
    Wandering = auto(),
    OutOfBounds = auto(),


class SimpleAnts:
    food: Food

    def __init__(self, spawn_pheromone: add_pheromone) -> None:
        self.position = np.zeros((SIZE, 2))
        self.velocity = np.zeros((SIZE, 2))
        self.acceleration = np.zeros((SIZE, 2))
        self.direction = np.zeros((SIZE, 2))
        self.pheromone_timer = np.zeros((SIZE, 1))
        self.wandering_timer = np.zeros((SIZE, 1))
        self.amount: int = 0
        self.size = SIZE
        self.state: list[AntState] = list()
        self.spawn_pheromone = spawn_pheromone

    def add(self, position: Vector2):

        self.position[self.amount] = [position.x, position.y]
        x, y = random_normal_vector()
        self.direction[self.amount] = [x, y]
        self.pheromone_timer[self.amount] = (random() * PHEROMONE_DELAY)
        self.wandering_timer[self.amount] = (random() * WANDER_DELAY)
        self.state.append(AntState.Wandering)
        self.amount += 1

        if self.amount >= self.size:
            self.position = np.concatenate(
                (self.position, np.zeros((self.size, 2))))
            self.velocity = np.concatenate(
                (self.velocity, np.zeros((self.size, 2))))
            self.acceleration = np.concatenate(
                (self.acceleration, np.zeros((self.size, 2))))
            self.direction = np.concatenate(
                (self.direction, np.zeros((self.size, 2))))
            self.pheromone_timer = np.concatenate(
                (self.pheromone_timer, np.zeros((self.size, 1))))
            self.wandering_timer = np.concatenate(
                (self.wandering_timer, np.zeros((self.size, 1))))
            self.size *= 2

    def update(self, dt: float):
        apply_movement_physics(self.position, self.velocity,
                               self.acceleration, dt)

        self.acceleration = self.acceleration + self.direction * ANT_ACCELERATION

        self.pheromone_timer[0:self.amount] += dt
        self.wandering_timer[0:self.amount] += dt

    def draw(self, screen: Surface):
        for position in self.position[0:self.amount]:
            x, y = position
            draw.circle(screen, ANT_COLOR, (x, y), ANT_RADIUS)


def search_vision_cone(position: Vector2, direction: Vector2, targets: ChunkedData[Vector2]):
    dirs: list[tuple[float, int, Vector2]] = list()
    for i, target in targets.get_neighborhood(position):
        diff = target - position
        dist = diff.length_squared()
        if dist > VISION_RANGE**2:
            continue
        elif dist < ANT_RADIUS**2:
            dirs.append((dist, i, direction.copy()))
            continue
        dist = sqrt(dist)
        dir = diff / dist
        dot = direction.dot(dir)
        if dot > .3:
            dirs.append((dist, i, dir.copy()))
    return dirs


def apply_friction(velocity):

    d = np.tile(
        np.expand_dims(
            np.sum(velocity**2, axis=1),
            axis=1),
        (1, 2)
    )
    direction = np.divide(velocity, np.sqrt(d), where=(d != 0))
    force = d * MY  # my:  friction cof
    friction = -direction * force
    velocity += friction


def apply_movement_physics(position, velocity, acceleration, dt: float):
    apply_friction(velocity)
    velocity += acceleration * dt
    position += velocity * dt
    acceleration *= 0
