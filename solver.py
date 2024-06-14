import logic
import numpy as np

SCORE_ON_LOSS = -250
#TODO: make "move to rotation" transformation directly in make_move
callbacks = {0: "u",
    1: "l",
    2: "d",
    3: "r"}

def _get_spawn_variations(field):
    """Return list of fields, with block spawned on each differently"""
    zero_positions = [
            list(filter(
            lambda x: x[1] == 0, 
            [((i, j), field[i][j]) for j in range(len(field[i]))]
        ))
             for i in range(len(field))]

    zero_positions = [j[0] for i in zero_positions for j in i]
    next_move_fields = []
    for zero_pos in zero_positions:
        for number in (2,4):
            new_field = field.copy()
            new_field[zero_pos[0]][zero_pos[1]] = number
            next_move_fields.append(new_field)
    return next_move_fields


def _move_scores(field, depth):

    if not logic.has_moves(field):
        return SCORE_ON_LOSS

    mean_next_possible_move_scores = np.zeros((4,))
    move_scores = np.zeros((4,))
    for move in range(4):#u, d, r, l
        new_field, score = logic.make_move(field.copy(), callbacks[move])
        move_scores[move] = score
        possible_scores = np.array([])
        if depth > 1:
            for field in _get_spawn_variations(new_field):
                possible_scores = np.append(
                    possible_scores,
                    np.max(_move_scores(field, depth-1)))
            mean_next_possible_move_scores[move] = np.mean(possible_scores)
    return mean_next_possible_move_scores + move_scores


def best_move(field, depth) -> str:
    print(f"MOVE: {callbacks[np.argmax(_move_scores(field, depth))]}")
    return callbacks[np.argmax(_move_scores(field, depth))]