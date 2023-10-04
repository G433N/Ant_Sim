from typing import Callable
from ECS.system import Command, System
from ECS.util import Entity
from ECS.world import World
from ECS.world_object import WorldObject


class SetUpWorld:
    """
    To create a ECS world you first to set up the world, \n
    by adding system to a this class. \n
    When you are done use 'compile()' to get your ECS world
    """
    _systems: dict[type, list[System]]
    _types: list[type]
    _archetypes: dict[type, list[Entity]]

    def __init__(self) -> None:
        self._systems = dict()
        self._types = list()
        self._archetypes = dict()

    def compile(self) -> World:
        """
        Get World with the same systems
        """
        world = World(
            self._systems,
            self._archetypes,
            self._types,
        )
        return world

    def add_system[T: WorldObject](self, type: type[T], system: Callable[[T, float], Command | None]):
        """
        Adds system of type T to the World.\n
        T should inherit from WorldObject, the second argument in the system is delta time since last frame.\n
        Return Command to add or remove entites
        """
        if type in self._systems.keys():
            self._systems[type].append(system)
        else:
            self._systems[type] = [system]
            self._types.append(type)
            self._archetypes[type] = []
