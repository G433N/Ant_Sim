from typing import Callable, Final
from pygame import Surface, Vector2, draw
from data_types import Position

ANT_NEST_COLOR: Final = "orange"
ANT_NEST_RADIUS: Final = 25

ANT_NEST_MAX_SPAWN: Final = 100
ANT_NEST_SPAWN_RATE: Final = 2

type F = Callable[[Position, Position], None]


class Ant_Nets:
    position: list[Position]
    timer: list[float]
    spawned_ants: list[int]
    world_size: Vector2
    spawn: F

    def __init__(self, world_size: Vector2, spawn: F) -> None:
        self.world_size = world_size
        self.spawn = spawn
        self.position = list()
        self.timer = list()
        self.spawned_ants = list()

    def add(self, position: Position):
        self.position.append(position)
        self.timer.append(0)
        self.spawned_ants.append(0)

    def update(self, dt: float):

        for i, position in enumerate(self.position):
            self.timer[i] += dt
            time = self.timer[i]
            spawned = self.spawned_ants[i]
            if spawned < ANT_NEST_MAX_SPAWN and time > ANT_NEST_SPAWN_RATE:
                self.spawn(position.copy(), self.world_size)
                self.spawned_ants[i] += 1
                self.timer[i] = time % ANT_NEST_SPAWN_RATE

    def draw(self, screen: Surface):
        for position in self.position:
            draw.circle(screen, ANT_NEST_COLOR, position, ANT_NEST_RADIUS)
