from pygame import Vector2
from world import WorldObject


class Phermone(WorldObject):

    def __init__(self, position: Vector2):
        self.position = position
        self.radius = 2