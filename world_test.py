
from pygame import Vector2
from movment import Movment
from world import Commands, World, WorldObject


def f(obj: Movment, dt: float):
    print(f)
    t = obj.velocity * 2
    print(t)


def g(obj: WorldObject, dt: float):
    print(g)
    print(obj)
    c = Commands()

    c.add_object(WorldObject(Vector2(), dt, str(type(obj))))
    return c


w = World()
w.add_system("test", Movment, f)
w.add_system("test2", WorldObject, g)
w.add_object(Movment(Vector2(), 5, "red", Vector2(), Vector2()))
w.add_object(WorldObject(Vector2(), 5, "lol"))

w.run(1)
w.run(1)
print(w)
