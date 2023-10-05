from pygame import Vector2
from ECS.entity import NOT_INIT_ENTITY
from ECS.world_generator import WorldGenerator
from ECS.system import Command
from Objects.Componets.world_object import WorldObject
from Objects.Componets.movment import Movement


def f(obj: Movement, dt: float):
    print(f)
    t = obj.velocity * 2
    print(t)
    c = Command()
    c.queue_remove(obj.id)
    return c


def g(obj: WorldObject, dt: float):
    print(g)
    print(obj)


w = WorldGenerator()
w.add_system(Movement, f)
w.add_system(WorldObject, g)
w = w.compile()
w.spawn(Movement(NOT_INIT_ENTITY, Vector2(),
                5, "red", Vector2(), Vector2()))
w.spawn(WorldObject(NOT_INIT_ENTITY, Vector2(), 5, "lol"))

for x in range(5):
    w.run(1)

print([x for x in w.get_objects()])
