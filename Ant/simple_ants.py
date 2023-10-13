from dataclasses import dataclass
from enum import Enum, auto
from math import sqrt
from random import random
from typing import Final
from pygame import Surface, Vector2, draw
from Ant.Food.food import Food
from Ant.Pheromone.add_pheromone import add_pheromone
from Util.chunked_data import ChunkedData
from Util.globals import WORLD_SIZE
from Util.util import bounds, random_normal_vector

ANT_ACCELERATION: Final = 20
ANT_COLOR: Final = "black"
ANT_RADIUS: Final = 3

PHEROMONE_DELAY: Final = 1
MY: Final = 0.0002

WANDER_DELAY: Final = 3

TARGET_COLOR: Final = "blue"
TARGET_RADIUS: Final = 2

VISION_RANGE: Final = 25

"""
TODO
Random ant movement offset
Search for food
Return home with food
Switch pheromone type and internal state
follow pheromone
"""


class AntState(Enum):
    Searching = auto(),
    Wandering = auto(),
    OutOfBounds = auto(),


@dataclass(slots=True)
class cAnt:
    position: Vector2
    velocity: Vector2
    acceleration: Vector2
    direction: Vector2
    pheromone_timer: float
    wandering_timer: float
    state: AntState


class SimpleAnts:
    ants: list[cAnt]
    spawn_pheromone: add_pheromone
    food: Food

    def __init__(self, spawn_pheromone: add_pheromone) -> None:
        self.ants = list()
        self.spawn_pheromone = spawn_pheromone

    def add(self, position: Vector2):
        self.ants.append(
            cAnt(
                position,
                Vector2(),
                Vector2(),
                random_normal_vector(),
                random() * PHEROMONE_DELAY,
                random() * WANDER_DELAY,
                AntState(AntState.Wandering)
            )
        )

    def update(self, dt: float):

        for ant in self.ants:

            apply_movement_physics(ant, dt)

            foods: list[tuple[float, int, Vector2]] = list()

            if not bounds(ant.position):
                ant.direction.xy = (WORLD_SIZE/2 - ant.position).normalize()
                ant.state = AntState.OutOfBounds
            else:
                if ant.velocity.length_squared() != 0:
                    foods = search_vision_cone(
                        ant.position, ant.velocity.normalize(), self.food.position)

            match ant.state:
                case AntState.Wandering:

                    if len(foods):
                        ant.state = AntState.Searching

                    ant.wandering_timer += dt
                    time = ant.wandering_timer
                    if time >= WANDER_DELAY:
                        ant.direction.xy = random_normal_vector()
                        ant.wandering_timer = time % WANDER_DELAY

                case AntState.OutOfBounds:
                    if bounds(ant.position):
                        self.state = AntState.Wandering

                case AntState.Searching:
                    if len(foods):
                        foods.sort(key=lambda x: x[0])
                        ant.direction.xy = foods[0][2]
                        if foods[0][0] < ANT_RADIUS:
                            self.food.position.remove(foods[0][1])
                    else:
                        ant.state = AntState.Wandering

            ant.acceleration += ant.direction * ANT_ACCELERATION

            ant.pheromone_timer += dt
            time = ant.pheromone_timer
            if time >= PHEROMONE_DELAY:
                ant.pheromone_timer = time % PHEROMONE_DELAY
                self.spawn_pheromone(ant.position.copy())

    def draw(self, screen: Surface):
        for ant in self.ants:
            if not bounds(ant.position):
                continue
            draw.circle(screen, ANT_COLOR, ant.position, ANT_RADIUS)
            if ant.velocity.length_squared() < 1:
                continue
            draw.circle(screen, ANT_COLOR, ant.position +
                        ant.velocity.normalize() * ANT_RADIUS * 1.2, ANT_RADIUS * 0.8)


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


def apply_movement_physics(ant: cAnt, dt: float):
    apply_friction(ant.velocity)
    ant.velocity += ant.acceleration * dt
    ant.position += ant.velocity * dt
    ant.acceleration *= 0


def apply_friction(velocity: Vector2):
    if velocity.length_squared() < 1:
        return

    direction = velocity.normalize()
    force = velocity.length_squared() * MY  # my:  fricton cof
    friction = -direction * force
    velocity += friction
