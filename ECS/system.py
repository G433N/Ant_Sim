from typing import Any, Callable
from ECS.util import Entity, TempEntity
from ECS.world_object import WorldObject

type System = Callable[[Any, float], Command | None]


class Command:
    objects_to_add: list[WorldObject]
    entities_to_remove: list[Entity]
    _next_id: TempEntity

    def __init__(self) -> None:
        self.objects_to_add = list()
        self.entities_to_remove = list()
        self._next_id = TempEntity(0)

    def add_object(self, obj: WorldObject) -> TempEntity:
        id = self._next_id
        self._next_id = TempEntity(1 + id)
        self.objects_to_add.append(obj)
        return id

    def remove_entity(self, e: Entity):
        self.entities_to_remove.append(e)
