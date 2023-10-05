from dataclasses import dataclass
from ECS.entity import Entity, EntityID
from ECS.system import InternalSystem


@dataclass
class World:
    """
    The ECS World holds all entites/objects and systems\n
    Also controls all backend logic\n
    Should not be created manually, use WorldGenerator class instead
    """
    # Would be nice with sets insted of lists but then we would lose determinism
    _objects: dict[EntityID, Entity]
    _entities: list[EntityID]
    _spawn_queue: list[tuple[EntityID, Entity]]
    _removed_entities: list[EntityID]
    _remove_queue: list[EntityID]
    _next_id: EntityID
    _systems: dict[type, list[InternalSystem]]
    _archetypes: dict[type, list[EntityID]]
    _types: list[type]

    def __init__(self, system: dict[type, list[InternalSystem]], archetypes: dict[type, list[EntityID]], types: list[type]) -> None:
        self._objects = dict()

        self._entities = list()
        self._spawn_queue = list()

        self._removed_entities = list()
        self._remove_queue = list()

        self._next_id = EntityID(0)

        self._systems = system
        self._archetypes = archetypes
        self._types = types

    def run(self, dt: float) -> None:
        """
        Runs a frame (all system once on respective entities)\n 
        dt is delta time since last run call
        """
        self._update_objects()

        for t, entities in self._archetypes.items():
            for e in entities:
                obj = self._objects[e]
                for system in self._systems[t]:
                    commands = system(obj, dt)
                    if commands is None:
                        continue
                    for obj in commands.objects_to_add:
                        self.spawn(obj)
                    for e in commands.entities_to_remove:
                        self.queue_remove(e)

    def spawn(self, obj: Entity) -> EntityID:
        """
        Queues an entity to be added to the world\n
        The entity gets added at the start of the next frame\n
        Returns the entity id
        """
        if len(self._removed_entities) == 0:
            id = self._next_id
            self._next_id = EntityID(1 + id)
        else:
            id = self._removed_entities.pop()

        obj.id = id
        self._spawn_queue.append((id, obj))
        return id

    def queue_remove(self, id: EntityID):
        """
        Queues a entity to be removed\n
        The entity gets removed at the start of the next frame\n
        Raises ValueError if the entity is not present.
        """
        self._remove_queue.append(id)

    def _update_objects(self):
        """
        Private method that adds and removes all queued entities
        """
        while len(self._spawn_queue) > 0:
            id, obj = self._spawn_queue.pop()
            assert not id in self._objects.keys()
            self._objects[id] = obj
            self._entities.append(id)

            for t in self._types:
                if isinstance(obj, t):
                    self._archetypes[t].append(id)

        while len(self._remove_queue) > 0:
            e = self._remove_queue.pop()
            obj = self._objects.pop(e)
            self._entities.remove(e)

            for t in self._types:
                if isinstance(obj, t):
                    self._archetypes[t].remove(e)
            del obj

    def get_objects(self):
        """
        Methods to iterate through all objects in the world\n
        to do stuff that are not currently possible with systems
        """
        for id in self._entities:
            yield self._objects[id]
