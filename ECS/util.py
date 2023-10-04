from typing import NewType

Entity = NewType("Entity", int)
TempEntity = NewType("TempEntity", int)

NOT_INIT_ENTITY = Entity(-1)
