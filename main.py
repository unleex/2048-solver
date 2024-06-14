import logic
import numpy as np
import pygame
import solver
import time
import visual
WIDTH = 360  
HEIGHT = 360 
FPS = 30

pygame.init()
pygame.display.set_caption("\t2048")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.SysFont("dejavusans", 20)
screen.fill((0,0,0))
pygame.display.flip()

FIELD_SIZE = (4,4)
BLOCK_SIZE = 40
BLOCK_GAP = 1
BUTTON_SIZE = 40
assert FIELD_SIZE[0] == FIELD_SIZE[1], "Field must be square"

SOLVER_DEPTH = 2
SOLVER_MIN_MOVE_TIME = 0.5
def main(autospawn: bool, autosolve: bool) -> None:
  field: np.ndarray = np.zeros(FIELD_SIZE, dtype=int)
 
  while logic.has_moves(field):
    #avoid overwriting already existing blocks
    if autospawn: 
      spawnx, spawny = logic.spawn_block(field)
    else:
      spawnx, spawny = map(int, input("Enter block spawn position x,y").split(','))
      
    field[spawnx][spawny] = np.random.choice([2,4])
    screen.fill((0,0,0))
    visual.render_field(screen, font, field, BLOCK_SIZE, BLOCK_GAP)
    if not autosolve:
      button_positions = visual.render_buttons(screen, BUTTON_SIZE)
      width, height = screen.get_size()
    #button positions are relative to their surface, that is in the bottom right, so remap them to screen coordinate
      button_positions = [(i[0]+(width - BUTTON_SIZE*3),
                       (i[1]+(height - BUTTON_SIZE*3))) for i in button_positions]
      
    pygame.display.flip()
    start = time.time()
    
    if not autosolve:
      waiting_for_input = True
      while waiting_for_input:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            pygame.quit()
            waiting_for_input = False
            running = False
          elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos 
            move = logic.get_move(mouse_pos, button_positions, BUTTON_SIZE)
            if move is not None:
              waiting_for_input = False
    else:
      best_move: str = solver.best_move(field, SOLVER_DEPTH)
    
    new_field, score = logic.make_move(field.copy(), best_move)
    
    end = time.time()
    time.sleep((max(0, SOLVER_MIN_MOVE_TIME - (end - start))))
    #avoid spawning new blocks if nothing changed after move
    while np.allclose(field, new_field):
      visual.render_field(screen, font, field, BLOCK_SIZE, BLOCK_GAP)
      pygame.display.flip()
      waiting_for_input = True
      #TODO: remove this duplication of loop
      if not autosolve:
        waiting_for_input = True
        while waiting_for_input:
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
              pygame.quit()
              running = False
              waiting_for_input = False
              
            elif event.type == pygame.MOUSEBUTTONDOWN:
              mouse_pos = event.pos 
              rotation = logic.get_rotation(mouse_pos, button_positions, BUTTON_SIZE)
              if rotation is not None:
                waiting_for_input = False
      else:
        rotation = solver.best_move(field, SOLVER_DEPTH)
        
      new_field, score = logic.make_move(field.copy(), rotation)
      
    field = new_field
    clock.tick(FPS)
  print("Game over!")


if __name__ == "__main__":
  main(autospawn = True, autosolve = True)