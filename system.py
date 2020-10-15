import pygame
from sprites import *
import setting

class Mechanics:
    def __init__(self, game, map):
        self.game = game
        self.map = map

    def check_nb(self, mvt, x, y, iteration=0, direction="None"):
        flag = 0
        if mvt == -1 or x < 0 or x > 31 or y < 0 or y > 23:
            return
        if isinstance(self.map.__getitem__(x, y).foreground, Highlight):
            flag = 1
        if (isinstance(self.map.__getitem__(x, y).background, River) or isinstance(self.map.__getitem__(x, y).unit, Infantry)) and iteration != 0:
            return
        if iteration != 0 and flag == 0:
            self.map.__getitem__(x, y).new_foreground("highlight")

        if direction != "down":
            self.check_nb(mvt - 1, x, y - 1, iteration+1, "up") #up
        if direction != "right":
            self.check_nb(mvt - 1, x - 1, y, iteration+1, "left") #left
        if direction != "left":
            self.check_nb(mvt - 1, x + 1, y, iteration+1, "right") #right
        if direction != "up":
            self.check_nb(mvt - 1, x, y + 1, iteration+1, "down") #down





        # flag = 0
        # if mvt == -1:
        #     return
        # for sprite in self.game.all_sprites:
        #     # print(sprite.name)
        #     if sprite.rect.collidepoint(x*TILESIZE, y*TILESIZE):
        #         print("sprite collion with", sprite.name)
        #         if sprite.name == "highlight":
        #             flag = 1
        #             break
        #         if sprite.name == "wall" or (sprite.name == "player" and iteration != 0):
        #             # print("i returned")
        #             return
        #
        # if iteration != 0 and flag == 0:
        #     Highlight(self.game, x, y)
        #
        # self.check_nb(mvt - 1, x, y - 1, iteration+1) #up
        # self.check_nb(mvt - 1, x - 1, y, iteration+1) #left
        # self.check_nb(mvt - 1, x + 1, y, iteration+1) #right
        # self.check_nb(mvt - 1, x, y + 1, iteration+1) #down

        #parse a travers les voisin jusqua ce quil nest plus de movement
        #mets un highlight sur les cases qu'il peut embarquer, n'embarque pas sur les walls



