import interact
import solver
import keyboard

DEPTH = 2

field_pos = interact.set_field_pos()
keyboard.add_hotkey('space', exit)

while True:
    field = interact.read_field(field_pos)
    best_move = solver.best_move(field, DEPTH)
    interact.send_move(best_move)