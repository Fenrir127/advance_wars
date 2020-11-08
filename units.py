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


class Unit:
    def __init__(self):
        self.x = None
        self.y = None
        self.game = None
        self.player = None
        self.name = None
        self.fuel = None
        self.damage = None
        self.movement = None
        self.hp = None
        self.mvt_type = None
        self.sprite = None
        self.available = None

    def end_turn(self):
        if self.available:
            self.available.kill()
            self.available = None

    def new_turn(self):
        self.available = Available(self.game, self.x, self.y)

    def die(self):
        self.sprite.kill()
        if self.available:
            self.available.kill()

    def move(self, x, y):
        self.x = x
        self.y = y
        self.sprite.rect.x = x * TILESIZE
        self.sprite.rect.y = y * TILESIZE
        if self.available:
            self.available.rect.x = x * TILESIZE
            self.available.rect.y = y * TILESIZE


class Infantry(Unit):
    def __init__(self, player, game, x, y):
        super().__init__()  # the super init doesn't really do anything for now
        self.x = x
        self.y = y
        self.game = game
        self.player = player
        self.name = "Infantry"
        self.fuel = 99
        self.damage = 3
        self.movement = 3
        self.hp = 10
        self.mvt_type = INFANTRY      # All unit need a movement type, check settings for all movement types
        self.sprite = Infantry_sprite(game, x, y, self.player.ID)
        self.available = None


class Tank(Unit):
    def __init__(self, player, game, x, y):
        super().__init__()  # the super init doesn't really do anything for now
        self.x = x
        self.y = y
        self.game = game
        self.player = player
        self.name = "Tank"
        self.fuel = 70
        self.damage = 5
        self.movement = 6
        self.hp = 10
        self.mvt_type = TREAD        # All unit need a movement type, check settings for all movement types
        self.sprite = Tank_sprite(game, x, y, self.player.ID)
        self.available = None

