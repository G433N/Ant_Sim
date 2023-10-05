from typing import Protocol
from data_types import Position


class add_pheromone(Protocol):

    def __call__(self, position: Position) -> None:
        ...
