from typing import Final

from pygame import Vector2, draw, Surface


DECAY_RATE: Final = 1
MINIMUM_STRENGTH: Final = 4
MAXIMUM_STRENGTH: Final = 8

PHEROMONE_COLOR = "purple"


class Pheromones:

    position: list[Vector2]
    strength: list[float]

    def __init__(self) -> None:
        self.position = list()
        self.strength = list()

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
        for position, radius in zip(self.position, self.strength):
            draw.circle(screen, PHEROMONE_COLOR, position, radius)
