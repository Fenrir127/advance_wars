import pygame as pg
from setting import *

"""
This contains all the Classes for the sprites
This is mainly used to draw and not much else
"""


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
        # self.image = self.game.mountain_image
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
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
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


# ------------------------Units----------------------------


class Infantry_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "infantry"
        self.groups = game.unit_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.infantry_image
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    # def update(self):
    #     self.rect.x = self.x * TILESIZE
    #     self.rect.y = self.y * TILESIZE


class Tank_sprite(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "tank"
        self.groups = game.unit_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.tank_image
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    # def update(self):
    #     self.rect.x = self.x * TILESIZE
    #     self.rect.y = self.y * TILESIZE


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
        self.game.map.unhighlight_tile(self.x, self.y)
        self.kill()
