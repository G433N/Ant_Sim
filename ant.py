from dataclasses import dataclass

from pygame import Vector2
from movment import Movment


@dataclass
class Ant(Movment):
    target: Vector2
    
    def __init__(self, positon: Vector2, target: Vector2) -> None:
        self.position = positon
        self.velocity = Vector2()
        self.acceleration = Vector2()
        self.color = "red"
        self.radius = 5
        self.target = target
        
