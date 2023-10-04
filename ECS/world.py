from dataclasses import dataclass
from ECS.System import System
from ECS.util import Entity
from ECS.world_object import WorldObject


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

    def __init__(self, system: dict[type, list[System]], archetypes: dict[type, list[WorldObject]], types: list[type]) -> None:
        self._objects = dict()

        self._entities = list()
        self._entities_to_add = list()

        self._removed_entities = list()
        self._entities_to_remove = list()

        self._next_id = Entity(0)
        self._no_more_systems = False

        self._systems = system
        self._archetypes = archetypes
        self._types = types

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
