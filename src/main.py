import interact
import solver
from pynput import keyboard
import pyautogui


def on_press(key):
    if key == keyboard.Key.esc:
        globals().update({'running': False})
        return False
    

DEPTH = 3
field_pos = interact.set_field_pos()
listener = keyboard.Listener(
    on_press=on_press)
listener.start()
running = True
while running:
    field = interact.read_field(field_pos)
    best_move = solver.best_move(field, DEPTH)
    if best_move != "no moves":
        pyautogui.press(best_move)
    else:
        running = False