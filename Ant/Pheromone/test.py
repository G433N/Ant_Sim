

from grid_chunking import Chunk_Grid

chunks = Chunk_Grid()

print(chunks)

chunks.add(2)

print(chunks)

chunks.flip(20)
chunks.flip(21)
chunks.flip(22)
chunks.flip(36)
chunks.flip(37)
chunks.flip(38)
chunks.flip(52)
chunks.flip(53)
chunks.flip(54)

print(chunks)

chunks.flip(20)
chunks.flip(22)
chunks.remove(37)
chunks.flip(52)
chunks.flip(54)

print(chunks)

