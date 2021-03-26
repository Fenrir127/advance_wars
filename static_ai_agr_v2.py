from setting import *
from os import path
import random

grid_x = GRID_X_SIZE
grid_y = GRID_Y_SIZE
unit_mvt = 3  # Infantry
legal_move = []

map_init = []
with open(path.join(path.dirname(__file__), MAP_TO_LOAD), 'rt') as f1:
    for line in f1:
        map_init.append(line.strip())

converter = {'w': 1, 'r': 2, 'p': 1, 'm': 2, 'd': 1, 's': 10}

mvt_cost_map = [[0 for x in range(GRID_X_SIZE)] for y in range(GRID_Y_SIZE)]
for x in range(GRID_X_SIZE):
    for y in range(GRID_Y_SIZE):
        mvt_cost_map[y][x] = converter[map_init[y][x]]


def get_action(x, y, hp, enx, eny, enhp):
    global unit_mvt
    get_legal_move(unit_mvt, x, y, enx, eny)
    global legal_move
    best_moves = []
    closest_moves = []
    second_closest_moves = []
    third_closest_moves = []
    final_moves = []
    if hp >= enhp:
        current_best_move_score = 999
        for move in legal_move:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score < current_best_move_score:
                current_best_move_score = total_score

        for move in legal_move:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score == current_best_move_score:
                best_moves.append((move[0], move[1]))
        pick = random.randint(0, len(best_moves) - 1)
        current_best_move_xy = best_moves[pick]

        if current_best_move_score == 1:  # In range to attack
            dx = enx - current_best_move_xy[0]
            dy = eny - current_best_move_xy[1]
        else:  # Not in range, move as close as possible
            current_best_move_score = 999
            best_moves.clear()
            for move in legal_move:
                if ((move[0] == 1 or move[0] == 5) and 1 <= move[1] <= 5) or (
                        (move[1] == 1 or move[1] == 5) and 1 <= move[0] <= 5):
                    best_moves.append((move[0], move[1]))
            for move in best_moves:
                dx = enx - move[0]
                dy = eny - move[1]
                total_score = abs(dx) + abs(dy)
                if total_score < current_best_move_score:
                    current_best_move_score = total_score

            for move in best_moves:
                dx = enx - move[0]
                dy = eny - move[1]
                total_score = abs(dx) + abs(dy)
                if total_score == current_best_move_score:
                    closest_moves.append((move[0], move[1]))
                elif total_score == current_best_move_score + 1:
                    second_closest_moves.append((move[0], move[1]))
                elif total_score == current_best_move_score + 2:
                    third_closest_moves.append((move[0], move[1]))
            for move in closest_moves:
                dx = x - move[0]
                dy = y - move[1]
                mvt_used = abs(dx) + abs(dy)
                if mvt_used == 3:
                    final_moves.append((move[0], move[1]))
            if not final_moves:
                for move in second_closest_moves:
                    dx = x - move[0]
                    dy = y - move[1]
                    mvt_used = abs(dx) + abs(dy)
                    if mvt_used == 3:
                        final_moves.append((move[0], move[1]))
            if not final_moves:
                for move in third_closest_moves:
                    dx = x - move[0]
                    dy = y - move[1]
                    mvt_used = abs(dx) + abs(dy)
                    if mvt_used == 3:
                        final_moves.append((move[0], move[1]))
            if len(final_moves) == 1:
                pick = 0
            else:
                pick = random.randint(0, len(final_moves) - 1)
            current_best_move_xy = final_moves[pick]
            dx = 0
            dy = 0

    else:
        current_best_move_score = 0
        for move in legal_move:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score > current_best_move_score:
                current_best_move_score = total_score
        best_moves = []
        for move in legal_move:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score == current_best_move_score:
                best_moves.append((move[0], move[1]))
        pick = random.randint(0, len(best_moves) - 1)
        current_best_move_xy = best_moves[pick]
        dx = 0
        dy = 0

    legal_move.clear()
    best_moves.clear()
    closest_moves.clear()
    second_closest_moves.clear()
    third_closest_moves.clear()
    final_moves.clear()
    return current_best_move_xy[0], current_best_move_xy[1], dx, dy


def get_legal_move(mvt, x, y, enx, eny, direction="None"):
    global mvt_cost_map
    global legal_move
    if mvt < 0 or x < 0 or x > GRID_X_SIZE - 1 or y < 0 or y > GRID_Y_SIZE - 1:
        return

    if x == enx and y == eny:
        return
    if (x, y) not in legal_move:
        legal_move.append((x, y))

    if direction != "down":
        if y - 1 >= 0:
            mvt_cost = mvt_cost_map[y - 1][x]
            get_legal_move(mvt - mvt_cost, x, y - 1, enx, eny, "up")  # going up
    if direction != "right":
        if x - 1 >= 0:
            mvt_cost = mvt_cost_map[y][x - 1]
            get_legal_move(mvt - mvt_cost, x - 1, y, enx, eny, "left")  # going left
    if direction != "left":
        if x + 1 <= GRID_X_SIZE - 1:
            mvt_cost = mvt_cost_map[y][x + 1]
            get_legal_move(mvt - mvt_cost, x + 1, y, enx, eny, "right")  # going right
    if direction != "up":
        if y + 1 <= GRID_Y_SIZE - 1:
            mvt_cost = mvt_cost_map[y + 1][x]
            get_legal_move(mvt - mvt_cost, x, y + 1, enx, eny, "down")  # going down


def test_get_legal_move(map_to_load, mvt,  x, y, enx, eny):
    _map_init = []
    with open(path.join(path.dirname(__file__), map_to_load), 'rt') as _f1:
        for _line in _f1:
            _map_init.append(_line.strip())

    _mvt_cost_map = [[0 for _x in range(7)] for _y in range(7)]
    for _x in range(7):
        for _y in range(7):
            _mvt_cost_map[_y][_x] = converter[_map_init[_y][_x]]

    moves = []
    alternate_get_legal(_mvt_cost_map, moves, mvt, x, y, enx, eny)
    return moves


def alternate_get_legal(cost_map, moves, mvt, x, y, enx, eny, direction="None", iteration=0):
    if direction != "None":
        iteration += 1
    if mvt < 0 or x < 0 or x > 7 - 1 or y < 0 or y > 7 - 1:
        return

    if x == enx and y == eny:
        return
    if (x, y) not in moves:
        moves.append((x, y))
    if direction != "down":
        if y - 1 >= 0:
            mvt_cost = cost_map[y - 1][x]
            alternate_get_legal(cost_map, moves, mvt - mvt_cost, x, y - 1, enx, eny, "up")  # going up
    if direction != "right":
        if x - 1 >= 0:
            mvt_cost = cost_map[y][x - 1]
            alternate_get_legal(cost_map, moves, mvt - mvt_cost, x - 1, y, enx, eny, "left")  # going left
    if direction != "left":
        if x + 1 <= GRID_X_SIZE - 1:
            mvt_cost = cost_map[y][x + 1]
            alternate_get_legal(cost_map, moves, mvt - mvt_cost, x + 1, y, enx, eny, "right")  # going right
    if direction != "up":
        if y + 1 <= GRID_Y_SIZE - 1:
            mvt_cost = cost_map[y + 1][x]
            alternate_get_legal(cost_map, moves, mvt - mvt_cost, x, y + 1, enx, eny, "down")  # going down
    if iteration == 0:
        return moves

def test_get_action(moves, x, y, hp, enx, eny, enhp):
    best_moves = []
    closest_moves = []
    second_closest_moves = []
    third_closest_moves = []
    final_moves = []

    if hp >= enhp:
        current_best_move_score = 999
        for move in moves:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score < current_best_move_score:
                current_best_move_score = total_score

        for move in moves:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score == current_best_move_score:
                best_moves.append((move[0], move[1]))
        pick = random.randint(0, len(best_moves) - 1)
        current_best_move_xy = best_moves[pick]

        if current_best_move_score == 1:  # In range to attack
            dx = enx - current_best_move_xy[0]
            dy = eny - current_best_move_xy[1]
        else:  # Not in range, move as close as possible
            current_best_move_score = 999
            best_moves.clear()
            for move in moves:
                if ((move[0] == 1 or move[0] == 5) and 1 <= move[1] <= 5) or (
                        (move[1] == 1 or move[1] == 5) and 1 <= move[0] <= 5):
                    best_moves.append((move[0], move[1]))
            for move in best_moves:
                dx = enx - move[0]
                dy = eny - move[1]
                total_score = abs(dx) + abs(dy)
                if total_score < current_best_move_score:
                    current_best_move_score = total_score

            for move in best_moves:
                dx = enx - move[0]
                dy = eny - move[1]
                total_score = abs(dx) + abs(dy)
                if total_score == current_best_move_score:
                    closest_moves.append((move[0], move[1]))
                elif total_score == current_best_move_score + 1:
                    second_closest_moves.append((move[0], move[1]))
                elif total_score == current_best_move_score + 2:
                    third_closest_moves.append((move[0], move[1]))
            for move in closest_moves:
                dx = x - move[0]
                dy = y - move[1]
                mvt_used = abs(dx) + abs(dy)
                if mvt_used == 3:
                    final_moves.append((move[0], move[1]))
            if not final_moves:
                for move in second_closest_moves:
                    dx = x - move[0]
                    dy = y - move[1]
                    mvt_used = abs(dx) + abs(dy)
                    if mvt_used == 3:
                        final_moves.append((move[0], move[1]))
            if not final_moves:
                for move in third_closest_moves:
                    dx = x - move[0]
                    dy = y - move[1]
                    mvt_used = abs(dx) + abs(dy)
                    if mvt_used == 3:
                        final_moves.append((move[0], move[1]))
            if len(final_moves) == 1:
                pick = 0
            else:
                pick = random.randint(0, len(final_moves) - 1)
            current_best_move_xy = final_moves[pick]
            dx = 0
            dy = 0

    else:
        current_best_move_score = 0
        for move in moves:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score > current_best_move_score:
                current_best_move_score = total_score
        best_moves = []
        for move in moves:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score == current_best_move_score:
                best_moves.append((move[0], move[1]))
        pick = random.randint(0, len(best_moves) - 1)
        current_best_move_xy = best_moves[pick]
        dx = 0
        dy = 0

    best_moves.clear()
    closest_moves.clear()
    second_closest_moves.clear()
    third_closest_moves.clear()
    final_moves.clear()
    moves.clear()
    return current_best_move_xy[0], current_best_move_xy[1], dx, dy