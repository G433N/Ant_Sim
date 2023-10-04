from dataclasses import dataclass
from typing import Any, Callable, NewType
from pygame import Vector2

Entity = NewType("Entity", int)
TempEntity = NewType("TempEntity", int)
type System = Callable[[Any, float], Commands | None]


@dataclass
class WorldObject:
    position: Vector2
    radius: float
    color: str


class Commands:
    entities: list[WorldObject]
    _entities_to_remove: list[Entity]
    _next_id: TempEntity

    def __init__(self) -> None:
        self.entities = list()
        self._entities_to_remove = list()
        self._next_id = TempEntity(0)

    def add_object(self, obj: WorldObject) -> TempEntity:
        id = self._next_id
        self._next_id = TempEntity(1 + id)
        self.entities.append(obj)
        return id


@dataclass
class World:

    _objects: dict[Entity, WorldObject]
    _entities: list[Entity]
    _entities_to_add: list[tuple[Entity, WorldObject]]
    _removed_entities: list[Entity]
    _entities_to_remove: list[Entity]
    _next_id: Entity
    _no_more_systems: bool
    _systems: dict[type, list[System]]
    _archetypes: dict[type, list[WorldObject]]
    _types: list[type]

    def __init__(self) -> None:
        self._objects = dict()

        self._entities = list()
        self._entities_to_add = list()

        self._removed_entities = list()
        self._entities_to_remove = list()

        self._next_id = Entity(0)
        self._no_more_systems = False

        self._systems = dict()
        self._archetypes = dict()
        self._types = list()

    def run(self, dt: float) -> None:
        self._update_objects()

        for t, objects in self._archetypes.items():
            for obj in objects:
                for f in self._systems[t]:
                    commands = f(obj, dt)
                    if commands is None:
                        continue
                    for obj in commands.entities:
                        self.add_object(obj)

    def add_object(self, obj: WorldObject) -> Entity:
        self._no_more_systems = False
        if len(self._removed_entities) == 0:
            id = self._next_id
            self._next_id = Entity(1 + id)
        else:
            id = self._removed_entities.pop()

        self._entities_to_add.append((id, obj))
        return id

    def add_system[T: WorldObject](self, type: type[T], system: Callable[[T, float], Commands | None]):
        # Make this enforced by the type system later
        assert not self._no_more_systems, "Don't and system after objects"
        if type in self._systems.keys():
            self._systems[type].append(system)
        else:
            self._systems[type] = [system]
            self._types.append(type)
            self._archetypes[type] = []

    def _update_objects(self):
        while len(self._entities_to_add) > 0:
            id, obj = self._entities_to_add.pop()
            assert not id in self._objects.keys()
            self._objects[id] = obj
            self._entities.append(id)

            for t in self._types:
                if isinstance(obj, t):
                    self._archetypes[t].append(obj)

    def get_objects(self):
        for id in self._entities:
            yield self._objects[id]
