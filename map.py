import pygame as pg
from setting import *
from os import path
from sprites import *
from units import *
from terrains import *


class Map:
    """
    Map has a 32x 24y grid of the gameworld and the terrain, units and highlight in it. It contains all this information
    and takes care of giving information to Game. It also takes care of moving units and such actions.
    """

    def __init__(self, game, testing):
        if testing:
            global MAP_TO_LOAD
            global PLAYER1_UNIT_TO_LOAD
            global PLAYER2_UNIT_TO_LOAD
            MAP_TO_LOAD = testing
            PLAYER1_UNIT_TO_LOAD = 'player1_test.txt'
            PLAYER2_UNIT_TO_LOAD = 'player2_test.txt'

        self.game = game
        self.map = [[0 for x in range(GRID_X_SIZE)] for y in range(GRID_Y_SIZE)]
        self.map_terrain = []  # temporary array that hold the info of terrains.txt while we copy it
        self.map_player1_unit = []  # temporary array that hold the info of units.txt while we copy it
        if NB_PLAYER != 1:
            self.map_player2_unit = []  # temporary array that hold the info of units.txt while we copy it
        map_init = path.dirname(__file__)
        with open(path.join(map_init, MAP_TO_LOAD), 'rt') as f1, open(path.join(map_init, PLAYER1_UNIT_TO_LOAD), 'rt') as f2, \
                open(path.join(map_init, PLAYER2_UNIT_TO_LOAD), 'rt') as f3:
            for line in f1:
                self.map_terrain.append(line.strip())  # reads and copies the file to the array
            for line in f2:
                self.map_player1_unit.append(line.strip())  # reads and copies the file to the array
            if NB_PLAYER != 1:
                for line in f3:
                    self.map_player2_unit.append(line.strip())  # reads and copies the file to the array

        """ this goes through the map array, create tiles for each square and gives which unit and terrain they are
        # we use the 2 temporary array map_terrain and map_unit to instantiate the Tile object in each
        # position of the array. I didn't figure out a way to read both text files at the same time and instantiate 
        # the Tile so I had to do this. Feel free to improve it"""

        for x in range(0, GRID_X_SIZE):
            for y in range(0, GRID_Y_SIZE):
                self.map[y][x] = Tile(self.game, self.map_terrain[y][x], x, y)  # , map_unit[y][x],
        for x in range(0, GRID_X_SIZE):
            for y in range(0, GRID_Y_SIZE):
                self.get_tile(x, y).add_unit(self.game.player1, self.map_player1_unit[y][x])
        if NB_PLAYER != 1:
            for x in range(0, GRID_X_SIZE):
                for y in range(0, GRID_Y_SIZE):
                    self.get_tile(x, y).add_unit(self.game.player2, self.map_player2_unit[y][x])

    def reset(self, _x=None, _y=None, enx=None, eny=None):
        del self.map
        self.map = [[0 for x in range(GRID_X_SIZE)] for y in range(GRID_Y_SIZE)]
        for x in range(0, GRID_X_SIZE):
            for y in range(0, GRID_Y_SIZE):
                self.map[y][x] = Tile(self.game, self.map_terrain[y][x], x, y)
        if _x != None and _y != None:
            self.get_tile(_x, _y).add_unit(self.game.player1, 'i')
        if enx != None and eny != None:
            self.get_tile(enx, eny).add_unit(self.game.player2, 'i')
        # for x in range(0, GRID_X_SIZE):
        #     for y in range(0, GRID_Y_SIZE):
        #         self.get_tile(x, y).add_unit(self.game.player1, self.map_player1_unit[y][x])
        #         self.get_tile(x, y).add_unit(self.game.player2, self.map_player2_unit[y][x])

    def get_tile(self, x, y):  # returns reference to a tile on the map
        return self.map[y][x]

    def get_mvt(self, x, y):  # returns unit movement for a unit on a tile
        return self.get_tile(x, y).unit.movement

    def get_unit_mvt_type(self, x, y):  # returns the type of mvt for a unit on a tile
        return self.get_tile(x, y).unit.mvt_type

    def get_terrain(self, x, y):  # returns reference to a terrain for a tile
        return self.get_tile(x, y).terrain

    def get_unit(self, x, y):  # returns reference to a unit on a tile
        return self.get_tile(x, y).unit

    def get_unit_name(self, x, y):  # returns unit name
        return self.get_tile(x, y).unit.name

    def get_terrain_name(self, x, y):  # returns terrain name
        return self.get_tile(x, y).terrain.name

    def get_defense(self, x, y):
        return self.get_tile(x, y).terrain.defense

    def get_tile_mvt_cost(self, mvt_type, x, y):  # returns mvt cost for a terrain for a given mvt_type on a given tile
        return self.get_tile(x, y).terrain.get_mvt_cost(mvt_type)

    def is_highlight(self, x, y):  # returns true if the tile is highlighted
        if x < 0 or x > GRID_X_SIZE - 1 or y < 0 or y > GRID_Y_SIZE - 1:
            return False
        return self.get_tile(x, y).highlighted

    def is_atk_highlight(self, x, y):  # returns true if the tile is highlighted with an atk_highlight
        if x < 0 or x > GRID_X_SIZE - 1 or y < 0 or y > GRID_Y_SIZE - 1:
            return False
        return self.get_tile(x, y).atk_highlighted

    def highlight_tile(self, x, y):  # highlights a tile
        if not self.get_tile(x, y).highlighted:
            self.get_tile(x, y).highlighted = Highlight(self.game, x, y)

    def atk_highlight_tile(self, x, y):  # atk highlights a tile
        if not self.get_tile(x, y).atk_highlighted:
            # print((x, y))
            self.get_tile(x, y).atk_highlighted = Atk_highlight(self.game, x, y)

    def atk_unhighlight_tile(self, x, y):  # atk unhighlights a tile
        self.get_tile(x, y).atk_highlighted.kill()
        self.get_tile(x, y).atk_highlighted = None

    def unhighlight_tile(self, x, y):  # unhighlights a tile
        self.get_tile(x, y).highlighted.kill()
        self.get_tile(x, y).highlighted = None
        self.get_tile(x, y).fuel_cost = 0

    def is_unit(self, x, y):  # returns if a tile has a unit on it
        if self.get_tile(x, y).unit:
            return True

    def move_unit(self, x1, y1, x2, y2):  # moves a unit to another tile
        if 0 > x2 > GRID_X_SIZE - 1 or 0 > y2 > GRID_Y_SIZE or 0 > x1 > GRID_X_SIZE - 1 or 0 > y1 > GRID_Y_SIZE:
            print("You tried to move a unit out of bound")
            print("x1, y1, x2, y2:")
            print(x1, y1, x2, y2)
            return
        unit = self.get_unit(x1, y1)

        unit.move(x2, y2)
        self.get_tile(x1, y1).unit = None
        self.get_tile(x2, y2).unit = unit

    def embark_unit(self, x, y):  # embark a unit on a transport unit
        tile = self.get_tile(x, y)
        tile.unit.embark()
        tile.unit = None

    def drop_unit(self, x, y, unit):  # drop a unit from a transport
        tile = self.get_tile(x, y)
        unit.drop(x, y)
        tile.unit = unit

    def remove_unit(self, x, y):  # Removes a unit from the game (because it's dead)
        tile = self.get_tile(x, y)
        if tile.unit.type == APC or tile.unit.type == TCOPTER or tile.unit.type == LANDER:
            if tile.unit.holding:
                tile.unit.player.units.remove(tile.unit.holding)
                tile.unit.holding.die()
                del tile.unit.holding
        tile.unit.player.units.remove(tile.unit)
        tile.unit.die()
        del tile.unit
        tile.unit = None

    def capture(self, x, y, player):  # Capture building
        self.get_tile(x, y).terrain.new_owner(player)

    def building_refuel(self, x, y):  # repairs for units on a friendly building tile
        if self.is_unit(x, y):
            unit = self.get_unit(x, y)
            building = self.get_tile(x, y).terrain
            if unit.player.ID == building.owner.ID:
                if building.type == unit.element:
                    unit.refuel()
                    unit.hp += 20
                    if unit.hp > FULL_HP:
                        unit.hp = FULL_HP

    """
    The Tile class takes care of holding all the information available within one tile of the map
    it doesn't do much expect that
    """


class Tile:
    def __init__(self, game, terrain, x, y):
        self.game = game
        self.highlighted = None  # this indicates if the tile is highlighted
        self.atk_highlighted = None  # this indicates if the tile is highlighted for an attack
        self.unit = None
        self.fuel_cost = 0
        self.x = x
        self.y = y
        self.terrain = self.id_terrain(terrain)

    def add_unit(self, player, type):
        # determines which unit type this tile should have and creates it, we use the letter from
        # the units.txt file in this coordinate to identify the right unit, as there are more unit implemented,
        # this function will have to be update to identify the new units
        if type == 'i':
            self.unit = Infantry(player, self.game, self.x, self.y)
            player.units.append(self.unit)
        elif type == 't':
            self.unit = Tank(player, self.game, self.x, self.y)
            player.units.append(self.unit)
        elif type == 'a':
            self.unit = Apc(player, self.game, self.x, self.y)
            player.units.append(self.unit)
        elif type == 'r':
            self.unit = Artillery(player, self.game, self.x, self.y)
            player.units.append(self.unit)
        elif type == 'n':
            self.unit = Recon(player, self.game, self.x, self.y)
            player.units.append(self.unit)
        elif type == 'm':
            self.unit = Mech(player, self.game, self.x, self.y)
            player.units.append(self.unit)
        elif type == 'T':
            self.unit = MDTank(player, self.game, self.x, self.y)
            player.units.append(self.unit)
        elif type == 'y':
            self.unit = Antiair(player, self.game, self.x, self.y)
            player.units.append(self.unit)
        elif type == 'l':
            self.unit = Missiles(player, self.game, self.x, self.y)
            player.units.append(self.unit)
        elif type == 'k':
            self.unit = Rockets(player, self.game, self.x, self.y)
            player.units.append(self.unit)
        elif type == '.':
            return None

    def id_terrain(self, type):
        # determines which terrain type this tile should have and creates it, we use the letter from
        # the terrains.txt file in this coordinate to identify the right terrain, as there are more terrain implemented,
        # this function will have to be update to identify the new terrains

        if type == 'p':
            return Plain(self.game, self.x, self.y)
        elif type == 'r':
            return River(self.game, self.x, self.y)
        elif type == 'w':
            return Wood(self.game, self.x, self.y)
        elif type == 'm':
            return Mountain(self.game, self.x, self.y)
        elif type == 's':
            return Sea(self.game, self.x, self.y)
        elif type == 'd':
            return Road(self.game, self.x, self.y)
        elif type == 'a':
            return City(self.game, self.x, self.y, self.game.player1)
        elif type == 'b':
            return City(self.game, self.x, self.y, self.game.player2)
        elif type == 'c':
            return City(self.game, self.x, self.y, None)
        elif type == 'R':
            return HQ(self.game, self.x, self.y, self.game.player1)
        elif type == 'B':
            return HQ(self.game, self.x, self.y, self.game.player2)
        elif type == 'h':
            return Beach(self.game, self.x, self.y)
        elif type == 'e':
            return Factory(self.game, self.x, self.y, self.game.player1)
        elif type == 'f':
            return Factory(self.game, self.x, self.y, self.game.player2)
        elif type == 'g':
            return Factory(self.game, self.x, self.y, None)
