import pygame as pg
from setting import *
import math
from os import path
from sprites import *

class Map:
    def __init__(self, game):
        self.game = game
        self.map = [[0 for i in range(32)] for j in range(24)]
        self.map_background = []
        self.map_unit = []
        map_init = path.dirname(__file__)
        with open(path.join(map_init,'background.txt'), 'rt') as f1, open(path.join(map_init,'unit.txt'), 'rt') as f2:
            for line in f1:
                self.map_background.append(line.strip())
            for line in f2:
                self.map_unit.append(line.strip())
        for x in range(0, 32):
            for y in range(0, 24):
                self.map[y][x] = Tile(self.game, self.map_background[y][x], self.map_unit[y][x], x, y)

    def __getitem__(self, x, y):
        return self.map[y][x]



class Tile:
    def __init__(self, game, background, unit, x, y):
        self.game = game
        self.background = self.id_background(self.game, background, x, y)
        self.unit = self.id_unit(self.game, unit, x, y)
        self.foreground = None
        self.x = x
        self.y = y

    def id_background(self, game, letter, x, y):
        if letter == 'p':
            return Plain(game, x, y)
        elif letter == 'r':
            return River(game, x, y)

    def id_unit(self,game, letter, x, y):
        if letter == 'i':
            return Infantry(game, x, y)

    def new_unit(self, name):
        if name == "infantry":
            if self.unit != None:
                self.unit.kill()
            self.unit = Infantry(self.game, self.x, self.y)
        else:
            print("unit is now none")
            self.unit.kill()
            self.unit = None

    def new_foreground(self, name):
        if name == "highlight":
            if self.foreground != None:
                self.foreground.kill()
            self.foreground = Highlight(self.game, self.x, self.y)
        elif self.foreground == None:
            pass
        else:
            self.foreground.kill()
            self.foreground = None

class Background:
    def __init__(self, type, x, y):
        self.type = type

class Unit:
    def __init__(self, type, x, y):
        self.type = type
    