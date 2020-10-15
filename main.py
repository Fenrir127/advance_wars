# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 1
# Project setup
# Video link: https://youtu.be/3UxnelT9aCo
import pygame as pg
import sys
from setting import *
from sprites import *
import math
import system
import random
from map import *
from os import path

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        self.load_data()

    def load_data(self):
        pass

    def new(self):
        # initialize all variables and do all the setup for a new game
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'image')
        self.infantry_image = pg.image.load(path.join(img_folder, 'mario.png')).convert_alpha()
        self.highlight_image = pg.image.load(path.join(img_folder, 'highlight.png')).convert_alpha()
        self.background_sprites = pg.sprite.Group()
        self.unit_sprites= pg.sprite.Group()
        self.foreground_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.highlight_list = pg.sprite.Group()
        self.plains = pg.sprite.Group()
        self.rivers = pg.sprite.Group()
        self.map = Map(self)
        self.system = system.Mechanics(self, self.map)
        # self.player = Player(self, 10, 10)
        # for x in range(10, 16):
        #     Wall(self, x, 5)
        # for x in range(17, 20):
        #     Wall(self, x, 5)
        # for x in range(10, 25):
        #     for y in range(0, 5):
        #         Wall(self, x, random.randint(1, 20))

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.unit_sprites.update()
        self.foreground_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.background_sprites.draw(self.screen)
        self.unit_sprites.draw(self.screen)
        self.foreground_sprites.draw(self.screen)
        # self.all_sprites.draw(self.screen)
        self.draw_grid()
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                # if event.key == pg.K_LEFT:
                #     self.player.move(dx=-1)
                # if event.key == pg.K_RIGHT:
                #     self.player.move(dx=1)
                # if event.key == pg.K_UP:
                #     self.player.move(dy=-1)
                # if event.key == pg.K_DOWN:
                #     self.player.move(dy=1)
            if event.type == pg.MOUSEBUTTONDOWN:
                x1, y1 = pg.mouse.get_pos()
                x1 = math.floor(x1 / TILESIZE)
                y1 = math.floor(y1 / 32)
                if isinstance(self.map.__getitem__(x1, y1).unit, Infantry):
                    self.highlight(self.map.__getitem__(x1, y1).unit.movement, x1, y1)
                    position_selected = False
                    while not position_selected:
                        event = pg.event.wait()
                        if event.type == pg.MOUSEBUTTONDOWN:
                            x2, y2 = pg.mouse.get_pos()
                            x2 = math.floor(x2 / 32)
                            y2 = math.floor(y2 / 32)
                            #print(isinstance(self.map.__getitem__(x2, y2).foreground, Highlight))
                            if isinstance(self.map.__getitem__(x2, y2).foreground, Highlight):
                                self.map.__getitem__(x1, y1).new_unit(None)
                                self.map.__getitem__(x2, y2).new_unit("infantry")
                            position_selected = True


                # if self.player.rect.collidepoint(x1, y1):
                #     x1 = math.floor(x1 / 32)
                #     y1 = math.floor(y1 / 32)
                #     self.highlight(self.player.movement, x1, y1)
                #     position_selected = False
                #     while not position_selected:
                #         event = pg.event.wait()
                #         if event.type == pg.MOUSEBUTTONDOWN:
                #             x2, y2 = pg.mouse.get_pos()
                #             for highlight in self.highlight_list:
                #                 if highlight.rect.collidepoint(x2, y2):
                #                     x2 = math.floor(x2 / 32)
                #                     y2 = math.floor(y2 / 32)
                #                     self.player.move_click(x2, y2)
                #             position_selected = True

    def highlight(self, mvt, x, y):
        self.system.check_nb(mvt, x, y)
        # for dy in range(y-mvt, y+mvt+1):
        #     for dx in range(x-mvt+(abs(y-dy)), x+mvt-(abs(y-dy))+1):
        #         if dx == x and dy == y:
        #             pass
        #         else:
        #             highlight = Highlight(self, dx, dy)
        #             self.highlight_list.add(highlight)
        #             # self.all_sprites.add(highlight)
        self.draw()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()