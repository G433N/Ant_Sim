from typing import Final

from pygame import Vector2, draw, Surface
import pygame


DECAY_RATE: Final = 1
MINIMUM_STRENGTH: Final = 4
MAXIMUM_STRENGTH: Final = 8

PHEROMONE_COLOR = "purple"
# TODO : Remove this file


class Pheromones:

    position: list[Vector2]
    strength: list[float]
    surface: Surface

    def __init__(self) -> None:
        self.position = list()
        self.strength = list()
        self.surface = Surface((5, 5), pygame.SRCALPHA)
        draw.circle(self.surface, PHEROMONE_COLOR, (3, 3), 2)

    def add(self, position: Vector2):
        self.position.append(position)
        self.strength.append(MAXIMUM_STRENGTH)

    def update(self, dt: float):
        strength = self.strength
        decay = DECAY_RATE * dt
        to_remove: list[int] = list()

        for i in range(len(strength)):
            strength[i] -= decay

            if strength[i] < MINIMUM_STRENGTH:
                to_remove.append(i)

        to_remove.sort()
        while len(to_remove) > 0:
            i = to_remove.pop()
            self.position.pop(i)
            self.strength.pop(i)

    def draw(self, screen: Surface):
        for position in self.position:
            screen.blit(self.surface, position)
