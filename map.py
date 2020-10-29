import pygame as pg
from setting import *
from os import path
from sprites import *
from units import *
from terrains import *


class Map:
    """
    Map has a 32x 24y grid of the gameworld and the terrain, units and highlight in it. It contains all this information
    and takes care of giving information to Game. It also takes care of moving units and such actions. Later on damage..
    """

    def __init__(self, game):
        self.game = game
        self.map = [[0 for x in range(32)] for y in range(24)]
        map_terrain = []  # temporary array that hold the info of terrains.txt while we copy it
        map_player1_unit = []  # temporary array that hold the info of units.txt while we copy it
        map_player2_unit = []  # temporary array that hold the info of units.txt while we copy it
        map_init = path.dirname(__file__)
        with open(path.join(map_init, 'terrain.txt'), 'rt') as f1, open(path.join(map_init, 'player1_unit.txt'), 'rt') as f2, \
                open(path.join(map_init, 'player2_unit.txt'), 'rt') as f3:
            for line in f1:
                map_terrain.append(line.strip())  # reads and copies the file to the array
            for line in f2:
                map_player1_unit.append(line.strip())  # reads and copies the file to the array
            for line in f3:
                map_player2_unit.append(line.strip())  # reads and copies the file to the array

        """ this goes through the map array, create tiles for each square and gives which unit and terrain they are
        # we use the 2 temporary array map_terrain and map_unit to instantiate the Tile object in each
        # position of the array. I didn't figure out a way to read both text files at the same time and instantiate 
        # the Tile so I had to do this. Feel free to improve it"""

        for x in range(0, 32):
            for y in range(0, 24):
                self.map[y][x] = Tile(self.game, map_terrain[y][x], x, y)  # , map_unit[y][x],
        for x in range(0, 32):
            for y in range(0, 24):
                self.get_tile(x, y).add_unit(PLAYER1, map_player1_unit[y][x])
        for x in range(0, 32):
            for y in range(0, 24):
                self.get_tile(x, y).add_unit(PLAYER2, map_player2_unit[y][x])

    def get_tile(self, x, y):  # returns reference to a tile on the map
        return self.map[y][x]

    def get_mvt(self, x, y):  # returns unit movement for a unit on a tile
        return self.get_tile(x, y).unit.movement

    def get_unit_mvt_type(self, x, y):  #returns the type of mvt for a unit on a tile
        return self.get_tile(x, y).unit.mvt_type

    def get_terrain(self, x, y):  # returns reference to a terrain for a tile
        return self.get_tile(x, y).terrain

    def get_unit(self, x, y):  # returns reference to a unit on a tile
        return self.get_tile(x, y).unit

    def get_unit_name(self, x, y): #returns unit name
        return self.get_tile(x, y).unit.name

    def get_terrain_name(self, x, y): #returns terrain name
        return self.get_tile(x, y).terrain.name

    def get_defense(self, x, y):
        return self.get_tile(x, y).terrain.defense

    def get_tile_mvt_cost(self, mvt_type, x, y):  # returns mvt cost for a terrain for a given mvt_type on a given tile
        return self.get_tile(x, y).terrain.get_mvt_cost(mvt_type)

    def is_highlight(self, x, y):  # returns if a tile is highlighted
        return self.get_tile(x, y).highlighted

    def is_atk_highlight(self, x, y):  # returns if a tile is highlighted
        return self.get_tile(x, y).atk_highlighted

    def highlight_tile(self, x, y):  # highlights a tile
        self.get_tile(x, y).highlighted = True
        Highlight(self.game, x, y)

    def atk_highlight_tile(self, x, y):
        self.get_tile(x, y).atk_highlighted = True
        Atk_highlight(self.game, x, y)

    def atk_unhighlight_tile(self, x, y):
        self.get_tile(x, y).atk_highlighted = False

    def unhighlight_tile(self, x, y):  # unhighlights a tile
        self.get_tile(x, y).highlighted = False

    def is_unit(self, x, y):  # returns if a tile has a unit on it
        if self.get_tile(x, y).unit:
            return True

    def move_unit(self, x1, y1, x2, y2):  # moves a unit to another tile
        unit = self.get_unit(x1, y1)
        unit.moved = not unit.moved
        unit.move(x2, y2)
        self.get_tile(x1, y1).unit = None
        self.get_tile(x2, y2).unit = unit
        if self.get_tile(x2, y2).terrain.name == "City":
            self.get_tile(x2, y2).terrain.owner = unit.player
            if unit.player == PLAYER1:
                self.game.player1_building.append(self.get_tile(x2, y2).terrain)
            elif unit.player == PLAYER2:
                self.game.player2_building.append(self.get_tile(x2, y2).terrain)


    def remove_unit(self, x, y):  # Removes a unit from the game (because it's dead)
        tile = self.get_tile(x, y)
        if tile.unit.player == PLAYER1:
            self.game.player1_units.remove(tile.unit)
        elif tile.unit.player == PLAYER2:
            self.game.player2_units.remove(tile.unit)
        tile.unit.die()
        tile.unit = None


    """
    The Tile class takes care of holding all the information available within one tile of the map
    it doesn't do much expect that
    """

class Tile:
    def __init__(self, game, terrain, x, y):
        self.game = game
        self.highlighted = False       #this indicates if the tile is highlighted
        self.atk_highlighted = False    #this indicates if the tile is highlighted for an attack
        self.unit = None
        self.x = x
        self.y = y
        self.terrain = self.id_terrain(terrain)


    def add_unit(self, player, type):
        # determines which unit type this tile should have and creates it, we use the letter from
        # the units.txt file in this coordinate to identify the right unit, as there are more unit implemented,
        # this function will have to be update to identify the new units
        if type == 'i':
            self.unit = Infantry(player, self.game, self.x, self.y)
            if player == PLAYER1:
                self.game.player1_units.append(self.unit)
            if player == PLAYER2:
                self.game.player2_units.append(self.unit)
        elif type == 't':
            self.unit = Tank(player, self.game, self.x, self.y)
            if player == PLAYER1:
                self.game.player1_units.append(self.unit)
            if player == PLAYER2:
                self.game.player2_units.append(self.unit)
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
        elif type == 'c':
            return City(self.game, self.x, self.y)





