from __future__ import annotations
from typing import NewType, Optional, Protocol
from ECS.entity import EntityID
from Objects.Componets.world_object import WorldObject

TempEntity = NewType("TempEntity", int)


# Make these two the same
class System[T](Protocol):
    def __call__(self, obj: T, dt: float) -> Optional[Command]:
        ...


class Command:
    """
    Use this class to remove or spawn entities from inside a system
    """
    objects_to_add: list[WorldObject]
    entities_to_remove: list[EntityID]
    _next_id: TempEntity

    def __init__(self) -> None:
        self.objects_to_add = list()
        self.entities_to_remove = list()
        self._next_id = TempEntity(0)

    def spawn(self, obj: WorldObject) -> TempEntity:
        """
        Queues an entity to be added to the world\n
        The entity gets added at the start of the next frame\n
        Returns a temporary entity id only valid this frame inside the system
        """
        id = self._next_id
        self._next_id = TempEntity(1 + id)
        self.objects_to_add.append(obj)
        return id

    def queue_remove(self, e: EntityID):
        """
        Queues a entity to be removed\n
        The entity gets removed at the start of the next frame\n
        Raises ValueError if the entity is not present.
        """
        self.entities_to_remove.append(e)
