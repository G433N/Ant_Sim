from enum import Enum, auto
from math import sqrt
from random import random
from typing import Final
from pygame import Surface, Vector2, draw
from Ant.Food.food import Food
from Ant.Pheromone.choose_direction import choose_direction
from Ant.Pheromone.add_pheromone import add_pheromone
from Ant.ant import Ant
from Util.chunked_data import ChunkedData
from Util.globals import WORLD_SIZE
from Util.movement import get_friction, apply_movement_physics
from Util.util import bounds, random_normal_vector

ANT_ACCELERATION: Final = 20
ANT_COLOR: Final = "black"
ANT_RADIUS: Final = 3

PHEROMONE_DROP_DISTANCE: Final = 5

WANDER_DELAY: Final = 0.5

TARGET_COLOR: Final = "blue"
TARGET_RADIUS: Final = 2

VISION_RANGE: Final = 10


class AntState(Enum):
    Searching = auto(),
    Wandering = auto(),
    OutOfBounds = auto(),
    # TODO : ReturnHome
    # TODO : ReturnHomeWithFood (drop food pheromone)


""" State machine
On start -> Wandering
Any -> OutOfBounds
OutOfBounds -> Wandering
Wandering -> (Searching OR ReturnHome)
Searching -> (ReturnHomeWithFood or Wandering)
ReturnHome -> (Searching or Wandering)
ReturnHomeWithFood -> Wandering
"""


class Add_Pheromone_Class:
    pass


class SimpleAnts(Ant):
    position: list[Vector2]
    velocity: list[Vector2]
    acceleration: list[Vector2]
    goal_direction: list[Vector2]
    pheromone_distance: list[float]
    wandering_timer: list[float]
    state: list[AntState]

    # TODO : This need to be a class instead with multiple named add_pheromone function, for multiple pheromones support
    spawn_pheromone: add_pheromone  # Name Add_Pheromones_Class or something better
    food: Food
    wander_direction: choose_direction

    def __init__(self, spawn_pheromone: add_pheromone, wander_direction: choose_direction) -> None:
        self.position = list()
        self.velocity = list()
        self.acceleration = list()
        self.goal_direction = list()
        self.pheromone_distance = list()
        self.wandering_timer = list()
        self.state = list()
        self.spawn_pheromone = spawn_pheromone
        self.wander_direction = wander_direction

    def add(self, position: Vector2):
        self.position.append(position)
        self.velocity.append(Vector2())
        self.acceleration.append(Vector2())
        self.goal_direction.append(random_normal_vector())
        self.pheromone_distance.append(random() * PHEROMONE_DROP_DISTANCE)
        self.wandering_timer.append(random() * WANDER_DELAY)
        self.state.append(AntState.Wandering)

    def update(self, dt: float):

        for i, (position, velocity, acceleration, goal_direction) in enumerate(zip(*self.movement_bundle(), self.goal_direction)):

            speed_squared = velocity.length_squared()
            speed = sqrt(speed_squared)

            direction = velocity / speed if speed else Vector2()

            velocity += get_friction(direction, speed_squared)
            apply_movement_physics(position, velocity, acceleration, dt)

            bound = bounds(position)
            foods: list[tuple[float, int, Vector2]] = list()

            if not bound:
                goal_direction.xy = (WORLD_SIZE/2 - position).normalize()
                self.state[i] = AntState.OutOfBounds
            else:
                if speed:
                    foods = search_vision_cone(
                        position, direction, self.food.position)

            match self.state[i]:  # TODO : Add new behavior to new states
                case AntState.Wandering:

                    if len(foods):
                        self.state[i] = AntState.Searching

                    self.wandering_timer[i] += dt
                    distance = self.wandering_timer[i]

                    if distance >= WANDER_DELAY:  # TODO : Make random ant movement sexier
                        goal_direction.xy = self.wander_direction(
                            goal_direction.xy, position)
                        self.wandering_timer[i] = distance % WANDER_DELAY

                case AntState.OutOfBounds:
                    if bound:
                        self.state[i] = AntState.Wandering

                case AntState.Searching:  # TODO : Add a timer for returning home without food
                    if len(foods):
                        foods.sort(key=lambda x: x[0])
                        goal_direction.xy = foods[0][2]

                        if foods[0][0] < ANT_RADIUS*2:
                            self.food.position.remove(foods[0][1])
                    else:
                        self.state[i] = AntState.Wandering

            acceleration += goal_direction * ANT_ACCELERATION

            acceleration += -direction * ANT_ACCELERATION * \
                (1 - direction.dot(goal_direction)) * 2/3

            self.pheromone_distance[i] += speed
            distance = self.pheromone_distance[i]

            if distance >= PHEROMONE_DROP_DISTANCE:
                self.pheromone_distance[i] = distance % PHEROMONE_DROP_DISTANCE
                # TODO : Switch function in Add_Pheromones_Class depending on state
                # TODO : We can add support for different timers and behaviors per pheromone later
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
        if dot > 0:
            dirs.append((dist, i, dir.copy()))
    return dirs
