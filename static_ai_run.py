from setting import *
from os import path
import random

grid_x = GRID_X_SIZE
grid_y = GRID_Y_SIZE
unit_mvt = 3  # Infantry
map_init = []
legal_move = []
dangerous_move = []

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
    if x == 4 and (y == 1 or y == 5) and enx == 3 and eny == 3:
        return x - 3, y, 0, 0

    get_legal_move(unit_mvt, x, y, enx, eny)
    get_vulnerable_tile(unit_mvt, enx, eny, x, y)
    global legal_move
    global dangerous_move

    best_moves = []
    for move in legal_move:
        if ((move[0] == 1 or move[0] == 5) and 1 <= move[1] <= 5) or ((move[1] == 1 or move[1] == 5) and 1 <= move[0] <= 5):
            best_moves.append((move[0], move[1]))

    # print(best_moves)
    for move in dangerous_move:
        if (move[0], move[1]) in best_moves:
            best_moves.remove((move[0], move[1]))
    # print(best_moves)
    if best_moves:
        current_best_move_score = 0
        for move in best_moves:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score > current_best_move_score:
                current_best_move_score = total_score
        final_moves = []
        for move in best_moves:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score == current_best_move_score:
                final_moves.append((move[0], move[1]))
        pick = random.randint(0, len(final_moves) - 1)
        current_best_move_xy = final_moves[pick]
    else:
        current_best_move_score = 0
        for move in legal_move:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score > current_best_move_score:
                current_best_move_score = total_score
        final_moves = []
        for move in legal_move:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score == current_best_move_score:
                final_moves.append((move[0], move[1]))
        pick = random.randint(0, len(final_moves) - 1)
        current_best_move_xy = final_moves[pick]
    legal_move.clear()
    dangerous_move.clear()
    best_moves.clear()
    final_moves.clear()
    return current_best_move_xy[0], current_best_move_xy[1], 0, 0


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


def check_surrounding(x, y):
    global dangerous_move
    if y - 1 >= 0 and (x, y - 1) not in dangerous_move:
        dangerous_move.append((x, y - 1))  # up
    if x - 1 >= 0 and (x - 1, y) not in dangerous_move:
        dangerous_move.append((x - 1, y))  # left
    if x + 1 <= GRID_X_SIZE - 1 and (x + 1, y) not in dangerous_move:
        dangerous_move.append((x + 1, y))  # right
    if y + 1 <= GRID_Y_SIZE - 1 and (x, y + 1) not in dangerous_move:
        dangerous_move.append((x, y + 1))  # down


def get_vulnerable_tile(mvt, x, y, enx, eny, direction="None"):
    global mvt_cost_map
    global dangerous_move
    global legal_move

    if x < 0 or x > GRID_X_SIZE - 1 or y < 0 or y > GRID_Y_SIZE - 1:  # if out of movement or out of the game grid, stop
        return

    if x == enx and y == eny:
        if (x, y) not in dangerous_move:
            dangerous_move.append((x, y))
        return

    check_surrounding(x, y)

    if mvt < 1:
        if (x, y) not in dangerous_move:
            dangerous_move.append((x, y))
        return

    if direction != "down":
        if y - 1 >= 0:
            mvt_cost = mvt_cost_map[y - 1][x]
            if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                get_vulnerable_tile(mvt - mvt_cost, x, y - 1, enx, eny, "up")  # going up
            else:
                if (x, y) not in dangerous_move:
                    dangerous_move.append((x, y))
    if direction != "right":
        if x - 1 >= 0:
            mvt_cost = mvt_cost_map[y][x - 1]
            if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                get_vulnerable_tile(mvt - mvt_cost, x - 1, y, enx, eny, "left")  # going up  # going left
            else:
                if (x, y) not in dangerous_move:
                    dangerous_move.append((x, y))
    if direction != "left":
        if x + 1 <= GRID_X_SIZE - 1:
            mvt_cost = mvt_cost_map[y][x + 1]
            if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                get_vulnerable_tile(mvt - mvt_cost, x + 1, y, enx, eny, "right")  # going up  # going right
            else:
                if (x, y) not in dangerous_move:
                    dangerous_move.append((x, y))
    if direction != "up":
        if y + 1 <= GRID_Y_SIZE - 1:
            mvt_cost = mvt_cost_map[y + 1][x]
            if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                get_vulnerable_tile(mvt - mvt_cost, x, y + 1, enx, eny, "down")  # going up  # going down
            else:
                if (x, y) not in dangerous_move:
                    dangerous_move.append((x, y))


def test_get_vulnerable_tile(map_to_load, mvt, x, y, enx, eny):
    _map_init = []
    with open(path.join(path.dirname(__file__), map_to_load), 'rt') as _f1:
        for _line in _f1:
            _map_init.append(_line.strip())

    _mvt_cost_map = [[0 for _x in range(7)] for _y in range(7)]
    for _x in range(7):
        for _y in range(7):
            _mvt_cost_map[_y][_x] = converter[_map_init[_y][_x]]

    dangerous_moves = []
    alternate_vulnerable_tile(_mvt_cost_map, dangerous_moves, mvt, enx, eny, x, y)
    return dangerous_moves


def alternate_vulnerable_tile(_mvt_cost_map, dangerous_moves, mvt, x, y, enx, eny, direction="None", iteration=0):

    if direction != "None":
        iteration += 1

    if x < 0 or x > 7 - 1 or y < 0 or y > 7 - 1:  # if out of movement or out of the game grid, stop
        return

    if x == enx and y == eny:
        if (x, y) not in dangerous_moves:
            dangerous_moves.append((x, y))
        return

    if y - 1 >= 0 and (x, y - 1) not in dangerous_moves:
        dangerous_moves.append((x, y - 1))  # up
    if x - 1 >= 0 and (x - 1, y) not in dangerous_moves:
        dangerous_moves.append((x - 1, y))  # left

    if x + 1 <= 7 - 1 and (x + 1, y) not in dangerous_moves:
        dangerous_moves.append((x + 1, y))  # right
    if y + 1 <= 7 - 1 and (x, y + 1) not in dangerous_moves:
        dangerous_moves.append((x, y + 1))  # down

    if mvt < 1:
        if (x, y) not in dangerous_moves:
            dangerous_moves.append((x, y))
        return

    if direction != "down":
        if y - 1 >= 0:
            mvt_cost = _mvt_cost_map[y - 1][x]
            if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                alternate_vulnerable_tile(_mvt_cost_map, dangerous_moves, mvt - mvt_cost, x, y - 1, enx, eny, "up")  # going up
            else:
                if (x, y) not in dangerous_moves:
                    dangerous_moves.append((x, y))
    if direction != "right":
        if x - 1 >= 0:
            mvt_cost = _mvt_cost_map[y][x - 1]
            if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                alternate_vulnerable_tile(_mvt_cost_map, dangerous_moves, mvt - mvt_cost, x - 1, y, enx, eny, "left")  # going left
            else:
                if (x, y) not in dangerous_moves:
                    dangerous_moves.append((x, y))
    if direction != "left":
        if x + 1 <= GRID_X_SIZE - 1:
            mvt_cost = _mvt_cost_map[y][x + 1]
            if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                alternate_vulnerable_tile(_mvt_cost_map, dangerous_moves, mvt - mvt_cost, x + 1, y, enx, eny, "right")  # going right
            else:
                if (x, y) not in dangerous_moves:
                    dangerous_moves.append((x, y))
    if direction != "up":
        if y + 1 <= GRID_Y_SIZE - 1:
            mvt_cost = _mvt_cost_map[y + 1][x]
            if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                alternate_vulnerable_tile(_mvt_cost_map, dangerous_moves, mvt - mvt_cost, x, y + 1, enx, eny, "down")  # going down
            else:
                if (x, y) not in dangerous_moves:
                    dangerous_moves.append((x, y))

    if iteration == 0:
        return dangerous_moves


def test_get_action(moves, vulnerable, x, y, hp, enx, eny, enhp):
    if x == 4 and (y == 1 or y == 5) and enx == 3 and eny == 3:
        return x - 3, y, 0, 0

    best_moves = []
    for move in moves:
        if ((move[0] == 1 or move[0] == 5) and 1 <= move[1] <= 5) or ((move[1] == 1 or move[1] == 5) and 1 <= move[0] <= 5):
            best_moves.append((move[0], move[1]))
    for move in vulnerable:
        if (move[0], move[1]) in best_moves:
            best_moves.remove((move[0], move[1]))
    if best_moves:
        current_best_move_score = 0
        for move in best_moves:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score > current_best_move_score:
                current_best_move_score = total_score
        final_moves = []
        for move in best_moves:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score == current_best_move_score:
                final_moves.append((move[0], move[1]))
        pick = random.randint(0, len(final_moves) - 1)
        current_best_move_xy = final_moves[pick]
    else:
        current_best_move_score = 0
        for move in moves:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score > current_best_move_score:
                current_best_move_score = total_score
        final_moves = []
        for move in moves:
            dx = enx - move[0]
            dy = eny - move[1]
            total_score = abs(dx) + abs(dy)
            if total_score == current_best_move_score:
                final_moves.append((move[0], move[1]))
        pick = random.randint(0, len(final_moves) - 1)
        current_best_move_xy = final_moves[pick]
    moves.clear()
    vulnerable.clear()
    best_moves.clear()
    final_moves.clear()
    return current_best_move_xy[0], current_best_move_xy[1], 0, 0
