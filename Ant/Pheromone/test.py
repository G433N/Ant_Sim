

from grid_chunking import Chunk_Grid

chunk = Chunk_Grid()

# chunk.add(index) 
# is for adding the chunk on that index to the active chunks
# (fastest of the three)

# chunk.remove(index) 
# is for removing the chunk on that index from the active chunks
# (prob slowest of the three)

# chunk.flipp(index)
# is for flipping the chunk on that index from active to inactive or vise versa 
# (prob faster than remove)