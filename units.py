from os import path
from sprites import *
from setting import *

"""
This contains all the information for the different units in the game
Nothing should change in there except maybe hp when we implement combat

When you implement a new unit to the game you need to:
    Make a new unit class
    make sure id_unit() in Tile can identify it from the .txt file (give it a letter ex. t for tank, make sure it's not already taken!!))
    create a sprite class for it (you can copy paste the template of infantry) i'll implement the image for the unit
"""

#TODO create a master class for all unit maybe?
# and implement new unit!

class Infantry:
    def __init__(self, game, x, y):
        self.name = "Infantry"
        self.fuel = 99
        self.damage = 3
        self.movement = 3
        self.hp = 10
        self.mvt_type = INFANTRY      #All unit need a movement type, check settings for all movement types
        self.sprite = Infantry_sprite(game, x, y)

class Tank:
    def __init__(self, game, x, y):
        self.name = "Tank"
        self.fuel = 99
        self.damage = 5
        self.movement = 6
        self.hp = 10
        self.mvt_type = TREAD        #All unit need a movement type, check settings for all movement types
        self.sprite = Tank_sprite(game, x, y)
