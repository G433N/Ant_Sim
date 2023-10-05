from typing import Final

import pygame
from data_types import Position


DECAY_RATE: Final = 0.15
MINIMUM_STRENGTH: Final = 5
MAXIMUM_STRENGTH: Final = 20

PHEROMONE_COLOR = "purple"


class Pheromones:

    position: list[Position]
    strength: list[float]

    def __init__(self) -> None:
        self.position = list()
        self.strength = list()

    def add(self, position: Position):
        self.position.append(position)
        self.strength.append(MAXIMUM_STRENGTH)

    def update(self, dt: float):
        strength = self.strength
        decay = 1 - DECAY_RATE * dt
        to_remove: list[int] = list()

        for i in range(len(strength)):
            strength[i] *= decay

            if strength[i] < MINIMUM_STRENGTH:
                to_remove.append(i)

        to_remove.sort()
        while len(to_remove) > 0:
            i = to_remove.pop()
            self.position.pop(i)
            self.strength.pop(i)

    def draw(self, screen: pygame.Surface):
        for position, radius in zip(self.position, self.strength):
            pygame.draw.circle(screen, PHEROMONE_COLOR, position, radius)
