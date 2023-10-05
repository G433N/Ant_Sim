from typing import NewType
from dataclasses import dataclass

EntityID = NewType("EntityID", int)
NOT_INIT_ENTITY = EntityID(-1)


@dataclass
class Entity:
    id: EntityID  # Should be set to -1
