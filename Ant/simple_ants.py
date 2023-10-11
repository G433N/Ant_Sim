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
from Util.movement import apply_movement_physics
from Util.util import bounds, random_normal_vector

ANT_ACCELERATION: Final = 20
ANT_COLOR: Final = "black"
ANT_RADIUS: Final = 3

PHEROMONE_DELAY: Final = 1

WANDER_DELAY: Final = 3

TARGET_COLOR: Final = "blue"
TARGET_RADIUS: Final = 2

VISION_RANGE: Final = 25

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


class SimpleAnts(Ant):
    position: list[Vector2]
    velocity: list[Vector2]
    acceleration: list[Vector2]
    direction: list[Vector2]
    pheromone_timer: list[float]
    wandering_timer: list[float]
    state: list[AntState]
    spawn_pheromone: add_pheromone
    food: Food

    def __init__(self, spawn_pheromone: add_pheromone) -> None:
        self.position = list()
        self.velocity = list()
        self.acceleration = list()
        self.direction = list()
        self.pheromone_timer = list()
        self.wandering_timer = list()
        self.state = list()
        self.spawn_pheromone = spawn_pheromone

    def add(self, position: Vector2):
        self.position.append(position)
        self.velocity.append(Vector2())
        self.acceleration.append(Vector2())
        self.direction.append(random_normal_vector())
        self.pheromone_timer.append(random() * PHEROMONE_DELAY)
        self.wandering_timer.append(random() * WANDER_DELAY)
        self.state.append(AntState.Wandering)

    def update(self, dt: float):

        for i, (position, velocity, acceleration, direction) in enumerate(zip(*self.movment_bundle(), self.direction)):

            apply_movement_physics(position, velocity, acceleration, dt)

            foods: list[tuple[float, int, Vector2]] = list()

            if not bounds(position):
                direction.xy = (WORLD_SIZE/2 - position).normalize()
                self.state[i] = AntState.OutOfBounds
            else:
                if velocity.length_squared() != 0:
                    foods = search_vision_cone(
                        position, velocity.normalize(), self.food.position)

            match self.state[i]:
                case AntState.Wandering:

                    if len(foods):
                        self.state[i] = AntState.Searching

                    self.wandering_timer[i] += dt
                    time = self.wandering_timer[i]
                    if time >= WANDER_DELAY:
                        direction.xy = random_normal_vector()
                        self.wandering_timer[i] = time % WANDER_DELAY

                case AntState.OutOfBounds:
                    if bounds(position):
                        self.state[i] = AntState.Wandering

                case AntState.Searching:
                    if len(foods):
                        foods.sort(key=lambda x: x[0])
                        direction.xy = foods[0][2]
                        if foods[0][0] < ANT_RADIUS:
                            self.food.position.remove(foods[0][1])
                    else:
                        self.state[i] = AntState.Wandering

            acceleration += direction * ANT_ACCELERATION

            self.pheromone_timer[i] += dt
            time = self.pheromone_timer[i]
            if time >= PHEROMONE_DELAY:
                self.pheromone_timer[i] = time % PHEROMONE_DELAY
                self.spawn_pheromone(position.copy())

    def draw(self, screen: Surface):
        for position, velocity in zip(self.position, self.velocity):
            if not bounds(position):
                continue
            draw.circle(screen, ANT_COLOR, position, ANT_RADIUS)
            if velocity.length_squared() < 1:
                continue
            draw.circle(screen, ANT_COLOR, position +
                        velocity.normalize() * ANT_RADIUS * 1.2, ANT_RADIUS * 0.8)


def search_vision_cone(position: Vector2, direction: Vector2, targets: ChunkedData[Vector2]):
    dirs: list[tuple[float, int, Vector2]] = list()
    for i, target in targets.get_neighbourhood(position):
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
