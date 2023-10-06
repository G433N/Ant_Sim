
from pygame import Surface, Vector2, draw
from Ant.ant import Ant
from Ant.simple_ants import ANT_ACCELERATION, ANT_COLOR, ANT_RADIUS
from Util.movement import apply_movement_physics


class TestAnts(Ant):
    position: list[Vector2]
    velocity: list[Vector2]
    acceleration: list[Vector2]
    world_size: Vector2
    mouse_position: Vector2

    def __init__(self, world_size: Vector2, mouse_pos: Vector2) -> None:
        self.world_size = world_size
        self.mouse_position = mouse_pos
        self.position = list()
        self.velocity = list()
        self.acceleration = list()

    def add(self, position: Vector2):
        self.position.append(position)
        self.velocity.append(Vector2())
        self.acceleration.append(Vector2())

    def update(self, dt: float):
        target = self.mouse_position
        for position, velocity, acceleration in zip(*self.movment_bundle()):
            apply_movement_physics(position, velocity, acceleration, dt)
            if position.distance_squared_to(target) < 10**2:
                continue

            dir = (target - position).normalize()
            acceleration += dir * ANT_ACCELERATION

    def draw(self, screen: Surface):
        for position in self.position:
            draw.circle(screen, ANT_COLOR, position, ANT_RADIUS)
