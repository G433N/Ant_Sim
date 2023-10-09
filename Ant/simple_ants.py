from math import pi, sqrt
from random import random
from typing import Final
from pygame import Surface, Vector2, draw
from Ant.Food.food import FOOD_SIZE, Food
from Ant.Pheromone.add_pheromone import add_pheromone
from Ant.ant import Ant
from Util.chunked_data import ChunkedData
from Util.movement import apply_movement_physics
from Util.util import bounds

ANT_ACCELERATION: Final = 150
ANT_COLOR: Final = "black"
ANT_RADIUS: Final = 5

PHEROMONE_DELAY: Final = .5

TARGET_COLOR: Final = "blue"
TARGET_RADIUS: Final = 2

VISION_RANGE: Final = 100

"""
TODO
Random ant movement offset
Search for food
Return home with food
Switch phermone type and internal state
follow phermone
"""


class SimpleAnts(Ant):
    position: list[Vector2]
    velocity: list[Vector2]
    acceleration: list[Vector2]
    direction: list[Vector2]
    timer: list[float]
    spawn_pheromone: add_pheromone
    food: Food

    def __init__(self, spawn_pheromone: add_pheromone) -> None:
        self.position = list()
        self.velocity = list()
        self.acceleration = list()
        self.direction = list()
        self.timer = list()
        self.spawn_pheromone = spawn_pheromone

    def add(self, position: Vector2):
        self.position.append(position)
        self.velocity.append(Vector2())
        self.acceleration.append(Vector2())
        self.direction.append(Vector2(1, 0).rotate_rad(random() * 2 * pi))
        self.timer.append(0)

    def update(self, dt: float):

        for i, (position, velocity, acceleration, direction) in enumerate(zip(*self.movment_bundle(), self.direction)):
            apply_movement_physics(position, velocity, acceleration, dt)

            if bounds(position) and velocity.length_squared() != 0:
                dirs = search_vision_cone(
                    position, velocity.normalize(), self.food.position)

                if len(dirs) > 0:
                    dirs.sort(key=lambda x: x[0])
                    direction.xy = dirs[0][2]
                    if dirs[0][0] < ANT_RADIUS:
                        self.food.position.remove(dirs[0][1])

            acceleration += direction * ANT_ACCELERATION

            self.timer[i] += dt
            time = self.timer[i]
            if time >= PHEROMONE_DELAY:
                self.timer[i] = time % PHEROMONE_DELAY
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
        if dot > .5:
            dirs.append((dist, i, dir.copy()))
    return dirs
