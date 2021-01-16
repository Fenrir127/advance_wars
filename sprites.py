import pygame as pg
from setting import *

"""
This contains all the Classes for the sprites
This is mainly used to draw and not much else
"""

#TODO since most sprite are the same except for the actual image, we can compact almost all this code into 3 class.
# One for terrain, one for unit and one for highlight.

# ---------------------Terrains---------------------------

class Plain_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "plain"
        self.groups = game.terrain_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.plain_image
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class River_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "river"
        self.groups = game.terrain_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.river_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Wood_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "wood"
        self.groups = game.terrain_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.wood_image
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Mountain_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "mountain"
        self.groups = game.terrain_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.mountain_image
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Sea_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "sea"
        self.groups = game.terrain_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.sea_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Beach_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "beach"
        self.groups = game.terrain_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.beach_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Road_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "mountain"
        self.groups = game.terrain_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.road_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class City_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, owner):
        self.name = "city"
        self.groups = game.terrain_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if owner is None:
            self.image = self.game.city_neutral_image
        elif owner.ID == Red:
            self.image = self.game.city_red_image
        elif owner.ID == Blue:
            self.image = self.game.city_blue_image

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Factory_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, owner):
        self.name = "city"
        self.groups = game.terrain_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if owner is None:
            self.image = self.game.factory_neutral_image
        elif owner.ID == Red:
            self.image = self.game.factory_red_image
        elif owner.ID == Blue:
            self.image = self.game.factory_blue_image

        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Hq_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, owner):
        self.name = "hq"
        self.groups = game.terrain_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if owner.ID == Red:
            self.image = self.game.hq_red_image
        elif owner.ID == Blue:
            self.image = self.game.hq_blue_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# ------------------------Units----------------------------


class Infantry_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.name = "infantry"
        self.groups = game.unit_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if color == Red:
            self.image = self.game.infantry_red_image
        elif color == Blue:
            self.image = self.game.infantry_blue_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Tank_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.name = "tank"
        self.groups = game.unit_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if color == Red:
            self.image = self.game.tank_red_image
        elif color == Blue:
            self.image = self.game.tank_blue_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class APC_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.name = "APC"
        self.groups = game.unit_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if color == Red:
            self.image = self.game.apc_red_image
        elif color == Blue:
            self.image = self.game.apc_blue_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Artillery_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.name = "Artillery"
        self.groups = game.unit_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if color == Red:
            self.image = self.game.artillery_red_image
        elif color == Blue:
            self.image = self.game.artillery_blue_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Recon_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.name = "recon"
        self.groups = game.unit_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if color == Red:
            self.image = self.game.recon_red_image
        elif color == Blue:
            self.image = self.game.recon_blue_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Mech_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.name = "mech"
        self.groups = game.unit_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if color == Red:
            self.image = self.game.mech_red_image
        elif color == Blue:
            self.image = self.game.mech_blue_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class MDTank_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.name = "mech"
        self.groups = game.unit_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if color == Red:
            self.image = self.game.mdtank_red_image
        elif color == Blue:
            self.image = self.game.mdtank_blue_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Antiair_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.name = "mech"
        self.groups = game.unit_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if color == Red:
            self.image = self.game.antiair_red_image
        elif color == Blue:
            self.image = self.game.antiair_blue_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Missiles_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.name = "mech"
        self.groups = game.unit_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if color == Red:
            self.image = self.game.missiles_red_image
        elif color == Blue:
            self.image = self.game.missiles_blue_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Rockets_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.name = "mech"
        self.groups = game.unit_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if color == Red:
            self.image = self.game.rockets_red_image
        elif color == Blue:
            self.image = self.game.rockets_blue_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# ------------------------------Highlight--------------------------


class Highlight(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "highlight"
        self.groups = game.foreground_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.highlight_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        self.game.map.unhighlight_tile(self.x, self.y)
        self.kill()


class Atk_highlight(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "attack highlight"
        self.groups = game.foreground_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.attack_highlight_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        self.game.map.atk_unhighlight_tile(self.x, self.y)
        self.kill()

class Available(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "available highlight"
        self.groups = game.available_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.available_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Select(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "select"
        self.groups = game.available_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.select_image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


