import numpy as np
from typing import Literal

def get_move(mouse_pos,button_positions, button_size) -> str | None:
  #direction to number of rotations on 90° counterclockwise to make blocks always move down
  callbacks = {0: "u",
              1: "l",
              2: "d",
              3: "r"}
  
  for i in range(len(button_positions)):
    if (button_positions[i][0] + button_size >= mouse_pos[0] 
        and mouse_pos[0] >= button_positions[i][0] 
        and button_positions[i][1] + button_size>= mouse_pos[1] 
        and mouse_pos[1] >= button_positions[i][1]):
      return callbacks[i]
      

def spawn_block(field):
  choicex = list(range(len(field)))
  choicey = list(range(len(field[0])))
  spawnx, spawny = np.random.choice(choicex), np.random.choice(choicey)
  switch = 0
  while field[spawnx][spawny] != 0:
    if switch:
      del choicex[choicex.index(spawnx)]
    else:
      del choicey[choicey.index(spawny)]
    spawnx, spawny = np.random.choice(choicex), np.random.choice(choicey)
  return spawnx, spawny


def has_moves(field) -> bool:
    for i in range(len(field)):
      for j in range(len(field)):
        if field[i][j] == 0:
          return True
        if (i > 0 and field[i][j] == field[i-1][j] 
        or i < len(field)-1 and field[i][j] == field[i+1][j] 
        or j > 0 and field[i][j] == field[i][j-1]
        or j < len(field[i])-1 and field[i][j] == field[i][j+1]):
          return True
    return False


def make_move(field, move: Literal['u', 'd', 'r', 'l']) -> tuple[np.ndarray, int]:
  """Return a field after some move and return score"""

  rotation_times: dict[str, int] = {"u": 2,
    "d": 0,
    "r": 3,
    "l": 1}
  rotation = rotation_times[move]
  score = 0
  field = np.rot90(field, rotation)
  for i in range(len(field)-1,-1,-1):#iterate from bottom to form stacks, block on block
    for j in range(len(field)):
      if field[i][j] != 0:
        #prevent chain merging
        merged = []
        #check bottom blocks
        targeti = i
        for bottom in range(i+1, len(field)): 
          if field[bottom][j] == field[i][j] and not (i in merged or bottom in merged): 
            #merge
            field[i][j] += field[bottom][j] 
            score += field[i][j]
            field[bottom][j] = 0
            targeti += 1
            merged.append(i)
          #pass block
          elif field[bottom][j] == 0:
            targeti += 1

          else: 
            break

        field[targeti][j],field[i][j] = field[i][j],field[targeti][j]
        #rotate back to normal
  return np.rot90(field, 4-rotation), score
