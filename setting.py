# define some colors (R, G, B)
"""
    Settings, change settings here to modify the game environment. Some things shouldn't be modified. In general, only modify
    GRID_X_SIZE, GRID_Y_SIZE, TILESIZE, PLAYER1_UNIT_TO_LOAD, PLAYER2_UNIT_TO_LOAD and some colors.
    To use another size for the map, Change the GRID_X_SIZE and GRID_Y_SIZE to match the size of your map.
    Also, change the MAP_TO_LOAD, PLAYER1_UNIT_TO_LOAD, PLAYER2_UNIT_TO_LOAD to load the files you want.
    This hasn't been thoroughly tested
"""
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# game settings
SKYNET_VS_AI = 0
PVP = 1
SKYNET_VS_P = 2
SKYNET_VS_SKYNET = 3

# Static AIs
AGRESSIVE = 0

# Scenarios
RUNAWAY = 0
ATTACK = 1
STALEMATE = 2

# Map Sizes
SMALL = 0
NORMAL = 1

MAPSIZE = SMALL
GAMEMODE = SKYNET_VS_P
SCENARIO = STALEMATE

START_FROM_NEW = 1  # 0: Load a specific q_table to learn from; 1: start a new q_table
STARTING_TABLE = 'skynet_q_table.pickle'  # Doesnt matter if START_FROM_NEW = 1

LEARNING_SK1 = 1  # 1: load a q_table and learn; 0: load a q_table and exploit
Q_TABLE_NAME_SK1 = 'attack_q_table2.pickle'
LEARNING_SK2 = 0
Q_TABLE_NAME_SK2 = 'skynet_q_table_aggressive_ai_v1_0.pickle'

ITERATIVE_TRAINING = 0  # if you want to train Skynet on plain map for perfect attacks

if MAPSIZE == NORMAL:
    GRID_X_SIZE = 32
    GRID_Y_SIZE = 24
    MAP_TO_LOAD = 'terrain_32x24.txt'
    PLAYER1_UNIT_TO_LOAD = 'player1_unit_32x24.txt'
    PLAYER2_UNIT_TO_LOAD = 'player2_unit_32x24.txt'
elif MAPSIZE == SMALL:
    GRID_X_SIZE = 7
    GRID_Y_SIZE = 7
    MAP_TO_LOAD = 'terrain_1v1_7x7.txt'
    PLAYER1_UNIT_TO_LOAD = 'player1_unit_7x7.txt'
    PLAYER2_UNIT_TO_LOAD = 'player2_unit_7x7.txt'

if GAMEMODE == SKYNET_VS_AI:
    # TODO Change NO_DRAW if you want to see the AI move or not
    WAIT_TIME = 0.5
    NO_DRAW = True
    STOP_DRAW_AT = 50
    DRAW_EVERY = 10000
    NB_PLAYER = 2
    if SCENARIO == RUNAWAY:
        MAP_TO_LOAD = 'scenario_runaway.txt'
    elif SCENARIO == ATTACK:
        MAP_TO_LOAD = 'scenario_attack.txt'
    else:
        MAP_TO_LOAD = 'scenario_stalemate.txt'


if GAMEMODE == SKYNET_VS_SKYNET:
    # TODO Change NO_DRAW if you want to see the AI move or not
    WAIT_TIME = 0.1
    NO_DRAW = False
    STOP_DRAW_AT = 50
    DRAW_EVERY = 10000
    NB_PLAYER = 2
    AI_TO_LOAD = None

if GAMEMODE == PVP:
    WAIT_TIME = 0
    NO_DRAW = False
    NB_PLAYER = 2

if GAMEMODE == SKYNET_VS_P:
    WAIT_TIME = 0
    NO_DRAW = False
    NB_PLAYER = 2
    if SCENARIO == RUNAWAY:
        MAP_TO_LOAD = 'scenario_runaway.txt'
    elif SCENARIO == ATTACK:
        MAP_TO_LOAD = 'scenario_attack.txt'
    else:
        MAP_TO_LOAD = 'scenario_stalemate.txt'



TILESIZE = 32
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 512

GRID_WIDTH = GRID_X_SIZE * TILESIZE
GRID_HEIGHT = GRID_Y_SIZE * TILESIZE
FPS = 60
TITLE = "Basic Wars"
BGCOLOR = DARKGREY


# GRIDWIDTH = GRID_WIDTH / TILESIZE
# GRIDHEIGHT = HEIGHT / TILESIZE

# Players
PLAYER1 = 0
PLAYER2 = 1

# #Scenarios
# DISADVANTAGE = 0
# ADVANTAGE = 1
# NEUTRAL = 2

MAX_SCENARIO_TURN = 20

#ID = 0
#CO = 0
FUNDS = 1

# UNIT MVT TYPES
INFANTRY = 0
MECH = 1
TIRES = 2
TREAD = 3
AIR = 4
SHIP = 5
TRANSPORT = 6

# COs
NEUTRAL = 0
ANDY = 1
MAX = 2
SAMI = 3
NELL = 4
EAGLE = 5
DRAKE = 6
OLAF = 7
GRIT = 8
KANBEI = 9
SONJA = 10
STURM = 11

# Game General
FULL_HP = 100
STARTING_FUNDS = 10000

# Terrain types
LAND = 0
WATER = 2
BUILDING = 1

# Player colors
Red = 0
Blue = 1
Neutral = 2

# Building
CITY = 0
FACTORY = 1
AIRPORT = 2
PORT = 3
HQ = 4

# Unit element
# LAND = 0
# AIR = 4
# WATER = 2



# Units

# INFANTRY = 0
# MECH = 1
RECON = 2
TANK = 3
MDTANK = 4
ARTILLERY = 5
ROCKETS = 6
ANTIAIR = 7
MISSILES = 8
BCOPTER = 9
FIGHTER = 10
BOMBER = 11
CRUISER = 12
SUB = 13
BSHIP = 14
APC = 15
TCOPTER = 16
LANDER = 17

# THESE ARE THE EFFING !@#$ TABLES FOR DAMAGE
# TOOK ME FRICKING 2 HOURS TO MAKE BETTER BE GRATEFUL!!!!
# Do not change please, I will murder someone

# To access how much a unit deals damage to another, figure out which weapon it is using (Main or Alt) and
# search the table using this method main_wpn[defender type][attacker type]
# defender and attacker type are units value seen above Ex BCOPTER = 9
# If a 0 is returned, it means the unit can't attack target

MAIN = 0
ALT = 1

main_wpn = [
    [0, 0, 0, 0, 0, 90, 95, 105, 0, 0, 0, 110, 0, 0, 95],
    [0, 0, 0, 0, 0, 85, 90, 105, 0, 0, 0, 110, 0, 0, 90],
    [0, 85, 0, 85, 105, 80, 90, 60, 0, 55, 0, 105, 0, 0, 90],
    [0, 55, 0, 55, 85, 70, 85, 25, 0, 55, 0, 105, 0, 0, 85],
    [0, 15, 0, 15, 55, 45, 55, 10, 0, 25, 0, 105, 0, 0, 55],
    [0, 70, 0, 70, 105, 75, 80, 50, 0, 65, 0, 105, 0, 0, 80],
    [0, 85, 0, 85, 105, 80, 85, 45, 0, 65, 0, 105, 0, 0, 85],
    [0, 65, 0, 65, 105, 75, 85, 45, 0, 25, 0, 95, 0, 0, 85],
    [0, 85, 0, 85, 105, 80, 90, 55, 0, 65, 0, 105, 0, 0, 90],
    [0, 0, 0, 0, 0, 0, 0, 120, 120, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 65, 100, 0, 55, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 75, 100, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 5, 55, 65, 85, 0, 0, 55, 0, 85, 0, 25, 95],
    [0, 0, 0, 1, 0, 60, 85, 0, 0, 25, 0, 95, 90, 55, 95],
    [0, 0, 0, 1, 10, 40, 55, 0, 0, 25, 0, 75, 0, 55, 50],
    [0, 75, 0, 75, 105, 80, 80, 50, 0, 65, 0, 105, 0, 0, 80],
    [0, 0, 0, 0, 0, 0, 0, 120, 120, 0, 100, 0, 0, 0, 0],
    [0, 0, 0, 10, 35, 55, 60, 0, 0, 25, 0, 95, 0, 95, 95]
]

alt_wpn = [
    [55, 65, 70, 75, 105, 0, 0, 0, 0, 75, 0, 0, 0, 0, 0],
    [45, 55, 65, 70, 95, 0, 0, 0, 0, 75, 0, 0, 0, 0, 0],
    [12, 18, 35, 40, 45, 0, 0, 0, 0, 30, 0, 0, 0, 0, 0],
    [5, 6, 6, 6, 8, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [15, 32, 45, 45, 45, 0, 0, 0, 0, 25, 0, 0, 0, 0, 0],
    [25, 35, 55, 55, 55, 0, 0, 0, 0, 35, 0, 0, 0, 0, 0],
    [5, 6, 4, 5, 7, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
    [25, 35, 28, 30, 35, 0, 0, 0, 0, 35, 0, 0, 0, 0, 0],
    [7, 9, 10, 10, 12, 0, 0, 0, 0, 65, 0, 0, 115, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 55, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 65, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [14, 20, 45, 45, 45, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0],
    [30, 35, 35, 40, 45, 0, 0, 0, 0, 95, 0, 0, 115, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# this list is used to cycle through what units can be spawned from a factory
factory_units = [INFANTRY, MECH, RECON, APC, ARTILLERY, TANK, ANTIAIR, MISSILES, ROCKETS, MDTANK]
# airpot list
# sea port list

# Cost for each unit, used when spawning a unit in factory, airport, seaport
unit_costs = [1000, 3000, 4000, 7000, 16000, 6000, 15000, 8000, 12000, 9000, 20000, 22000, 18000, 20000, 28000, 5000, 5000, 12000]

# Max ammo for each unit, used when refueling by APC
max_ammo = [0, 3, 0, 9, 8, 9, 6, 9, 6, 6, 9, 9, 9, 6, 9, 0, 0, 0]

# Max fuel for each unit, used when refueling by APC
max_fuel = [99, 70, 80, 70, 50, 99, 50, 60, 50, 99, 99, 99, 99, 60, 99, 70, 99, 99]

# End of turn fuel cost (only for sea and air unit)
fuel_cost = [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 5, 5, 1, 1, 1, 0, 2, 1]

unit_name_symbol = [
    ("Infantry", 'i'),
    ("Mech", 'm'),
    ("Recon", 'n'),
    ("Tank", 't'),
    ("MdTank", 'T'),
    ("Artillery", 'r'),
    ("Rockets", 'k'),
    ("Antiair", 'y'),
    ("Missiles", 'l'),
    ("Battlecopter", 'i'),
    ("Fighter", 'i'),
    ("Bomber", 'i'),
    ("Cruise", 'i'),
    ("Sub", 'i'),
    ("Battleship", 'i'),
    ("APC", 'a'),
    ("Transport Copter", 'i'),
    ("Lander", 'i')
]