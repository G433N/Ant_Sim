from typing import Any, Callable
from ECS.util import Entity, TempEntity
from ECS.world_object import WorldObject

type System = Callable[[Any, float], Command | None]


class Command:
    """
    Use this class to remove or spawn entities from inside a system
    """
    objects_to_add: list[WorldObject]
    entities_to_remove: list[Entity]
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

    def queue_remove(self, e: Entity):
        """
        Queues a entity to be removed\n
        The entity gets removed at the start of the next frame\n
        Raises ValueError if the entity is not present.
        """
        self.entities_to_remove.append(e)
