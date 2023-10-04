from pygame import Vector2
from ECS.init_world import InitWorld
from ECS.util import NOT_INIT_ENTITY
from ECS.world_object import WorldObject
from Objects.Componets.movment import Movment


def f(obj: Movment, dt: float):
    print(f)
    t = obj.velocity * 2
    print(t)


def g(obj: WorldObject, dt: float):
    print(g)
    print(obj)


w = InitWorld()
w.add_system(Movment, f)
w.add_system(WorldObject, g)
w = w.compile()
w.add_object(Movment(NOT_INIT_ENTITY, Vector2(), 5, "red", Vector2(), Vector2()))
w.add_object(WorldObject(NOT_INIT_ENTITY, Vector2(), 5, "lol"))

w.run(1)
w.run(1)
print(w)
