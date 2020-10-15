import pygame as pg
from setting import *
import math


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "player"
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.movement = 4

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def move_click(self, dx, dy):
        self.x = dx
        self.y = dy

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "wall"
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Plain(pg.sprite.Sprite):
    def __init__(self, game, x, y):

        self.name = "plain"
        self.groups = game.background_sprites, game.plains
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class River(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "river"
        self.groups = game.background_sprites, game.rivers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Infantry(pg.sprite.Sprite):
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
        self.movement = 9

    # def move(self, dx=0, dy=0):
    #     self.x += dx
    #     self.y += dy

    # def move_click(self, dx, dy):
    #     self.game.map.__getitem__(self.x, self.y).new_unit(None)
    #     self.x = dx
    #     self.y = dy
    #     self.game.map.__getitem__(self.x, self.y).new_unit("infantry")

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Highlight(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.name = "highlight"
        self.groups = game.foreground_sprites, game.highlight_list
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.highlight_image
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        self.game.map.__getitem__(self.x, self.y).new_foreground(None)

# class Background(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.highlight
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         self.image = pg.Surface((TILESIZE, TILESIZE))
#         self.image.fill(DARKGREY)
#         self.rect = self.image.get_rect()
#         self.x = x
#         self.y = y
#         self.rect.x = x * TILESIZE
#         self.rect.y = y * TILESIZE
