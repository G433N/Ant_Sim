from typing import Callable
from ECS.system import Command, System
from ECS.util import Entity
from ECS.world import World
from ECS.world_object import WorldObject


class InitWorld:
    _systems: dict[type, list[System]]
    _types: list[type]
    _archetypes: dict[type, list[Entity]]

    def __init__(self) -> None:
        self._systems = dict()
        self._types = list()
        self._archetypes = dict()

    def compile(self) -> World:
        world = World(
            self._systems,
            self._archetypes,
            self._types,
        )
        del self
        return world

    def add_system[T: WorldObject](self, type: type[T], system: Callable[[T, float], Command|None]):
        if type in self._systems.keys():
            self._systems[type].append(system)
        else:
            self._systems[type] = [system]
            self._types.append(type)
            self._archetypes[type] = []