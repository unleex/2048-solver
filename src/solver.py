import logic
import numpy as np

SCORE_ON_LOSS = -250
SCORE_ON_STALL = float('-inf')

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


def _move_scores(field: np.ndarray, depth: int) -> dict[str, int]:

    if not logic.has_moves(field):
        return {"no moves": SCORE_ON_LOSS}

    move_scores = {"u": 0, "d": 0, "r": 0, "l": 0}
    for move in move_scores:
        new_field, score = logic.make_move(field.copy(), move)
        if np.allclose(field, new_field):
            move_scores[move] = SCORE_ON_STALL # make algorithm avoid this without inventing new logic
            continue
        move_scores[move] = score
        possible_scores = np.array([])
        if depth > 1:
            possible_scores = [np.max(list(_move_scores(possible_field, depth - 1).values()))
                               for possible_field in _get_spawn_variations(new_field)]
            move_scores[move] += np.mean(possible_scores)
    
    return move_scores


def best_move(field, depth) -> str:
    move_scores = _move_scores(field, depth)
    return max(move_scores, key=move_scores.get)