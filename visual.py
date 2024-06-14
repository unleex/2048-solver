import pygame

def render_field(screen, font, field, block_size, block_gap):
  for i in range(len(field)):
    for j in range(len(field[0])):

      left: int = j*(block_size+block_gap) 
      top: int = i*(block_size+block_gap)  
      rect = pygame.Rect(left, top, block_size, block_size)
      color_switch = field[i][j]%3
      color = [255,240,240]
      color[color_switch] -= field[i][j]*5
      pygame.draw.rect(screen, color, rect)
      numx = left + block_size//2 - (len(str(field[i][j])) - 1) * 6 - 5
      numy = top + block_size//2 - 5
      text = font.render(str(field[i][j]), True, (0,0,0))
      screen.blit(text, (numx, numy))


def render_buttons(screen, button_size):
  surface = pygame.Surface((button_size*3, button_size*3))

  surface.fill((255,255,255))
  #order: up, left, right, down
  button_positions = [(button_size, 0),
                     (0, button_size),
                     (button_size, button_size*2),
                     (button_size*2,button_size)]

  for pos in button_positions:
    rect = pygame.Rect(pos, (button_size, button_size))
    pygame.draw.rect(surface, (100,100,100), rect)

  width, height = screen.get_size()
  screen.blit(surface,(width - button_size*3,
                       height - button_size*3))
  return button_positions