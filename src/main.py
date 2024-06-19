import interact
import solver
import keyboard

DEPTH = 3

field_pos = interact.set_field_pos()
keyboard.add_hotkey('space', lambda: globals().update({'running': False})) # without lambda this stops working

running = True
while running:
    field = interact.read_field(field_pos)
    best_move = solver.best_move(field, DEPTH)
    if best_move != "no moves":
        interact.send_move(best_move)
    else:
        running = False