import interact
import solver
import keyboard
import pyautogui


DEPTH = 3
keyboard.add_hotkey('space', lambda: globals().update({'running': False}))
field_pos = interact.set_field_pos()
running = True
while running:
    field = interact.read_field(field_pos)
    best_move = solver.best_move(field, DEPTH)
    if best_move != "no moves":
        pyautogui.press(best_move)
    else:
        running = False