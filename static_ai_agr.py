from setting import *
from os import path

grid_x = GRID_X_SIZE
grid_y = GRID_Y_SIZE
unit_mvt = 3  # Infantry
map_init = []
legal_move = []

with open(path.join(path.dirname(__file__), MAP_TO_LOAD), 'rt') as f1:
    for line in f1:
        map_init.append(line.strip())

converter = {'w': 1, 'r': 2, 'p': 1, 'm': 2, 'd': 1, 's': 10}

mvt_cost_map = [[0 for x in range(GRID_X_SIZE)] for y in range(GRID_Y_SIZE)]
for x in range(GRID_X_SIZE):
    for y in range(GRID_Y_SIZE):
        mvt_cost_map[y][x] = converter[map_init[y][x]]


def get_action(x, y, enx, eny):
    global unit_mvt
    get_legal_move(unit_mvt, x, y, enx, eny)
    global legal_move
    current_best_move_xy = ()
    current_best_move_score = 999
    for move in legal_move:
        dx = enx - move[0]
        dy = eny - move[1]
        total_score = abs(dx) + abs(dy)
        if total_score < current_best_move_score:
            current_best_move_xy = (move[0], move[1])
            current_best_move_score = total_score
    if current_best_move_score == 1:  # In range to attack
        dx = enx - current_best_move_xy[0]
        dy = eny - current_best_move_xy[1]
    else:  # Not in range, move as close as possible
        dx = 0
        dy = 0

    legal_move.clear()
    return current_best_move_xy[0], current_best_move_xy[1], dx, dy


def get_legal_move(mvt, x, y, enx, eny, direction="None"):
    global mvt_cost_map
    global legal_move
    if mvt < 0 or x < 0 or x > GRID_X_SIZE - 1 or y < 0 or y > GRID_Y_SIZE - 1:
        return

    if x == enx and y == eny:
        return

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
