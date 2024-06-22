import numpy as np
from typing import Literal

def has_moves(field) -> bool:
    """
    Return true if a field has at least one empty tile
    and/or two equal neighbouring tiles.
    """
    for i in range(len(field) - 1):
      for j in range(len(field) - 1):
        if field[i][j] in (0, field[i + 1][j], field[i][j + 1]):
          return True
    return False


def make_move(field, move: Literal['up', 'down', 'right', 'left']) -> tuple[np.ndarray, int]:
  """Return field and score after some move made on it"""

  rotation_times: dict[str, int] = {"up": 2,
    "down": 0,
    "right": 3,
    "left": 1}
  rotation = rotation_times[move]
  score = 0
  field = np.rot90(field, rotation) # rotate the field to always make the move slide tiles down
  for i in range(len(field)-1,-1,-1): # iterate from bottom to form stacks, block on block
    for j in range(len(field)):
      if field[i][j] != 0:
        # prevent chain merging
        merged = []
        # check bottom blocks
        targeti = i
        for bottom in range(i+1, len(field)): 
          if field[bottom][j] == field[i][j] and not (i in merged or bottom in merged): 
            # merge
            field[i][j] += field[bottom][j] 
            score += field[i][j]
            field[bottom][j] = 0
            targeti += 1
            merged.append(i)
          elif field[bottom][j] == 0:
            targeti += 1
          else: 
            break

        field[targeti][j], field[i][j] = field[i][j], field[targeti][j]
  # rotate back to normal
  return np.rot90(field, 4-rotation), score
