import pickle

import pygame as pg
import sys
import Skynet as Skynet
import qlearning_mvmt_infantry as vsai
import numpy as np
from map import *
from os import path
import math
import random
import time
import static_ai_agr_v2 as agr_ai
import static_ai_run as run_ai


# TODO Change the name of all the highlight function to make more sense and be more readable, even I get confused


class Game:
    """Game has references to the Map and a list of all the sprites.
    Game takes care of all user interactions and calls map most of the time for information inquiries
    and changing the gameworld such as moving a unit."""

    def __init__(self):
        pg.init()

        # General game settings and initialization
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.iteration = 0
        self.success = 0
        self.load_data()  # used for future loading purposes

    def load_data(self):  # used for future loading purposes, does nothing for now
        pass

    def new(self):
        # initialize all variables and do all the setup for a new game
        # This is where we initialize the buttons and the text boxes
        self.textboxes = []
        self.unit_text = Textbox(self.screen, SCREEN_WIDTH-480, 0, 240, 256)
        self.textboxes.append(self.unit_text)
        self.terrain_text = Textbox(self.screen, SCREEN_WIDTH-240, 0, 240, 256)
        self.textboxes.append(self.terrain_text)
        if SCREEN_HEIGHT > 512:
            self.preview_text = Textbox(self.screen, SCREEN_WIDTH - 480, 256, 480, 256)
            self.textboxes.append(self.preview_text)
            self.cancel_btn = Button(self.screen, WHITE, SCREEN_WIDTH - 240, 640, 240, 128, "Cancel")
            if GAMEMODE == SKYNET_VS_SKYNET or GAMEMODE == SKYNET_VS_AI:
                self.end_turn_btn = Button(self.screen, WHITE, TILESIZE * GRID_X_SIZE + 20, 0, 240, 128, "End Turn")
            else:
                self.end_turn_btn = Button(self.screen, WHITE, SCREEN_WIDTH - 480, 640, 240, 128, "End Turn")
            self.special_btn = Button(self.screen, WHITE, SCREEN_WIDTH - 240, 512, 240, 128, "Cptr/Rfl/Mrg")
            self.attack_btn = Button(self.screen, WHITE, SCREEN_WIDTH - 480, 512, 240, 128, "Attack")
        else:
            self.preview_text = Textbox(self.screen, 0, 256, 480, 256)
            self.textboxes.append(self.preview_text)
            self.cancel_btn = Button(self.screen, WHITE, SCREEN_WIDTH - 240, 384, 240, 128, "Cancel")
            if GAMEMODE == SKYNET_VS_SKYNET or GAMEMODE == SKYNET_VS_AI:
                self.end_turn_btn = Button(self.screen, WHITE, TILESIZE * GRID_X_SIZE + 20, 0, 240, 128, "End Turn")
            else:
                self.end_turn_btn = Button(self.screen, WHITE, SCREEN_WIDTH - 480, 384, 240, 128, "End Turn")
            self.special_btn = Button(self.screen, WHITE, SCREEN_WIDTH - 240, 256, 240, 128, "Cptr/Rfl/Mrg")
            self.attack_btn = Button(self.screen, WHITE, SCREEN_WIDTH - 480, 256, 240, 128, "Attack")


        # This is where we create the buttons
        self.buttons_list = []

        self.buttons_list.append(self.cancel_btn)
        self.buttons_list.append(self.end_turn_btn)
        self.buttons_list.append(self.special_btn)
        self.buttons_list.append(self.attack_btn)

        # Game folders References
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'image')

        # General images import
        # Units
        self.infantry_red_image = pg.image.load(path.join(img_folder, 'infantry_red.png')).convert_alpha()
        self.infantry_blue_image = pg.image.load(path.join(img_folder, 'infantry_blue.png')).convert_alpha()
        self.tank_red_image = pg.image.load(path.join(img_folder, 'tank_red.png')).convert_alpha()
        self.tank_blue_image = pg.image.load(path.join(img_folder, 'tank_blue.png')).convert_alpha()
        self.apc_red_image = pg.image.load(path.join(img_folder, 'apc_red.png')).convert_alpha()
        self.apc_blue_image = pg.image.load(path.join(img_folder, 'apc_blue.png')).convert_alpha()
        self.artillery_red_image = pg.image.load(path.join(img_folder, 'artillery_red.png')).convert_alpha()
        self.artillery_blue_image = pg.image.load(path.join(img_folder, 'artillery_blue.png')).convert_alpha()
        self.recon_red_image = pg.image.load(path.join(img_folder, 'recon_red.png')).convert_alpha()
        self.recon_blue_image = pg.image.load(path.join(img_folder, 'recon_blue.png')).convert_alpha()
        self.mech_red_image = pg.image.load(path.join(img_folder, 'mech_red.png')).convert_alpha()
        self.mech_blue_image = pg.image.load(path.join(img_folder, 'mech_blue.png')).convert_alpha()
        self.mdtank_red_image = pg.image.load(path.join(img_folder, 'mdtank_red.png')).convert_alpha()
        self.mdtank_blue_image = pg.image.load(path.join(img_folder, 'mdtank_blue.png')).convert_alpha()
        self.antiair_red_image = pg.image.load(path.join(img_folder, 'antiair_red.png')).convert_alpha()
        self.antiair_blue_image = pg.image.load(path.join(img_folder, 'antiair_blue.png')).convert_alpha()
        self.missiles_red_image = pg.image.load(path.join(img_folder, 'missiles_red.png')).convert_alpha()
        self.missiles_blue_image = pg.image.load(path.join(img_folder, 'missiles_blue.png')).convert_alpha()
        self.rockets_red_image = pg.image.load(path.join(img_folder, 'rockets_red.png')).convert_alpha()
        self.rockets_blue_image = pg.image.load(path.join(img_folder, 'rockets_blue.png')).convert_alpha()

        # Terrain
        self.plain_image = pg.image.load(path.join(img_folder, 'plain.png')).convert_alpha()
        self.river_image = pg.image.load(path.join(img_folder, 'river.png')).convert_alpha()
        self.wood_image = pg.image.load(path.join(img_folder, 'wood.png')).convert_alpha()
        self.mountain_image = pg.image.load(path.join(img_folder, 'mountain.png')).convert_alpha()
        self.road_image = pg.image.load(path.join(img_folder, 'road.png')).convert_alpha()
        self.sea_image = pg.image.load(path.join(img_folder, 'sea.png')).convert_alpha()
        self.city_neutral_image = pg.image.load(path.join(img_folder, 'city_neutral.png')).convert_alpha()
        self.city_blue_image = pg.image.load(path.join(img_folder, 'city_blue.png')).convert_alpha()
        self.city_red_image = pg.image.load(path.join(img_folder, 'city_red.png')).convert_alpha()
        self.factory_neutral_image = pg.image.load(path.join(img_folder, 'factory_neutral.png')).convert_alpha()
        self.factory_blue_image = pg.image.load(path.join(img_folder, 'factory_blue.png')).convert_alpha()
        self.factory_red_image = pg.image.load(path.join(img_folder, 'factory_red.png')).convert_alpha()
        self.hq_blue_image = pg.image.load(path.join(img_folder, 'hq_blue.png')).convert_alpha()
        self.hq_red_image = pg.image.load(path.join(img_folder, 'hq_red.png')).convert_alpha()
        self.beach_image = pg.image.load(path.join(img_folder, 'beach.png')).convert_alpha()

        # Highlights
        self.highlight_image = pg.image.load(path.join(img_folder, 'highlight.png')).convert_alpha()
        self.attack_highlight_image = pg.image.load(path.join(img_folder, 'attack_highlight.png')).convert_alpha()
        self.available_image = pg.image.load(path.join(img_folder, 'available.png')).convert_alpha()
        self.select_image = pg.image.load(path.join(img_folder, 'select.png')).convert_alpha()

        # Sprite list setup
        self.terrain_sprites = pg.sprite.Group()
        self.unit_sprites = pg.sprite.Group()
        self.foreground_sprites = pg.sprite.Group()
        self.available_sprites = pg.sprite.Group()

        # In the last version, every sprite of the same kind was in a group of it's own.
        # This is unused for now but might come handy later on
        # self.infantry = pg.sprite.Group()
        # self.highlight_list = pg.sprite.Group()
        # self.plains = pg.sprite.Group()
        # self.rivers = pg.sprite.Group()

        # Initialize the players, first number is the player ID, second is the CO
        if GAMEMODE == SKYNET_VS_SKYNET:
            self.player1 = Player(PLAYER1, NEUTRAL)
            self.player2 = Player(PLAYER2, NEUTRAL)
            self.turn = PLAYER1  # Starting player is player 1
            self.players = [self.player1, self.player2]
            self.scenario_player_1 = None
            self.scenario_counter = 0
            self.next_reward = None
            self.scenarios = ["Stalemate", "Runaway", "Attack"]
            # if AI_TO_LOAD == AGRESSIVE:
            #     self.static_ai =
            # self.player1 = Player(PLAYER1, NEUTRAL)
            # self.turn = PLAYER1  # Starting player is player 1
            # self.players = [self.player1]
        elif GAMEMODE == SKYNET_VS_AI:
            self.player1 = Player(PLAYER1, NEUTRAL)
            self.player2 = Player(PLAYER2, NEUTRAL)
            self.turn = PLAYER1  # Starting player is player 1
            self.players = [self.player1, self.player2]
            self.scenario_counter = 0
            self.scenarios = ["Stalemate", "Runaway", "Attack"]
        elif GAMEMODE == SKYNET_VS_P:
            self.player1 = Player(PLAYER1, NEUTRAL)
            self.player2 = Player(PLAYER2, NEUTRAL)
            self.turn = PLAYER1  # Starting player is player 1
            self.players = [self.player1, self.player2]
            self.scenario_player_1 = None
            self.scenario_player_2 = None
            self.scenario_counter = 0
            self.scenarios = ["Stalemate", "Runaway", "Attack"]
        elif GAMEMODE == PVP:
            self.player1 = Player(PLAYER1, NEUTRAL)
            self.player2 = Player(PLAYER2, NEUTRAL)
            self.turn = PLAYER1  # Starting player is player 1
            self.players = [self.player1, self.player2]  # List of players, we could have more, need to add to the list and change settings
        # elif GAMEMODE == AI_VS_P:
        #     pass
        # elif NB_PLAYER == 1:
        #     self.player1 = Player(PLAYER1, NEUTRAL)
        #     self.turn = PLAYER1  # Starting player is player 1
        #     self.players = [self.player1]

        # creates the map and the reference
        self.map = Map(self)
        self.turn_counter = 0

    def run(self):
        # game loop, set self.playing = False to end the game
        self.playing = True
        if GAMEMODE == SKYNET_VS_SKYNET:
            self.get_random_scenario()
            self.skynet1 = Skynet.Skynet(1, 1, 1, 1, LEARNING_SK1)
            self.skynet2 = Skynet.Skynet(1, 1, 1, 1, LEARNING_SK2)
            self.q_table = np.zeros([7, 7, 7, 7] + [125])
            self.skynet1.set_q_table(self.q_table)
            self.skynet2.set_q_table(self.q_table)
            self.reset()
            self.turn_counter += 1
        elif GAMEMODE == SKYNET_VS_AI:
            self.skynet = Skynet.Skynet(1, 1, 1, 1)
            if not START_FROM_NEW:  # We want to load a specific q_table to train
                f = open(STARTING_TABLE, 'rb')
                self.q_table = pickle.loads(f.read())
            else:
                self.q_table = np.full([7, 7, 7, 7] + [125], -1)
            self.skynet.set_q_table(self.q_table)
            self.turn_counter += 1
            if SCENARIO == RUNAWAY:
                self.scenario_player_1 = 1
            elif SCENARIO == ATTACK:
                self.scenario_player_1 = 2
                self.iterative_training = ITERATIVE_TRAINING
            else:
                self.scenario_player_1 = 0
            self.reset()
        elif GAMEMODE == SKYNET_VS_P:
            self.skynet = Skynet.Skynet(1, 1, 1, 1)
            self.q_table = np.zeros([7, 7, 7, 7] + [125])
            self.skynet.set_q_table(self.q_table)
            self.reset()
            self.new_turn()
        # Hard coded, player 1 always start the game
        for unit in self.player1.units:
            unit.new_turn()
        self.draw()

        while self.playing:  # game loop
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            # self.erase_highlights()
            self.draw()

    """
    Only resets units and the map.
    """

    def reset(self):
        global NO_DRAW
        if GAMEMODE != SKYNET_VS_P:
            self.iteration += 1
            print("Iteration: " + str(self.iteration))
            if self.iteration % DRAW_EVERY == 0:
                NO_DRAW = False
            else:
                NO_DRAW = True

        self.turn_counter = 0
        for unit in self.player1.units:
            unit.die()
            self.player1.units.remove(unit)
        for unit in self.player2.units:
            unit.die()
            self.player2.units.remove(unit)
        if GAMEMODE == SKYNET_VS_AI:
            if SCENARIO == RUNAWAY:
                x, y = 0, 3
                enx, eny = 6, 3
                self.map.reset(x, y, enx, eny)
                self.scenario_counter = 0
                self.player1.units[0].hp = 10
                self.skynet.set_param(x, y, enx, eny)
            elif SCENARIO == ATTACK:
                if not self.iterative_training:
                    x, y = 6, 3
                    enx, eny = 0, 3
                    self.map.reset(x, y, enx, eny)
                    self.scenario_counter = 0
                    self.player2.units[0].hp = 10
                    self.skynet.set_param(x, y, enx, eny)
            else:
                x, y = self.get_random_pos()
                enx, eny = self.get_random_pos(x, y)
                self.map.reset(x, y, enx, eny)
                self.scenario_counter = 0
                self.skynet.set_param(x, y, enx, eny, )
            # x, y = self.get_random_pos()
            # enx, eny = self.get_random_pos(x, y)
            # self.map.reset(x, y, enx, eny)
            # self.scenario_player_1, self.scenario_player_2, lhp, rhp, rel_hp = self.get_random_scenario()
            # self.scenario_players = [self.scenario_player_1, self.scenario_player_2]
            # print("Scenario is " + self.scenarios[self.scenario_players[0]])
            # self.end_turn_btn.text = str(self.scenarios[self.scenario_players[1]])
            # self.scenario_counter = 0
            # if not lhp:
            #     self.player1.units[0].hp = 20
            # if not rhp:
            #     self.player2.units[0].hp = 20
            # self.skynet.set_param(x, y, rel_hp, enx, eny, )

        if GAMEMODE == SKYNET_VS_SKYNET:
            self.next_reward = None
            x, y = self.get_random_pos()
            enx, eny = self.get_random_pos(x, y)
            self.map.reset(x, y, enx, eny)
            self.scenario_player_1, self.scenario_player_2, lhp, rhp, = self.get_random_scenario()
            self.scenario_players = [self.scenario_player_1, self.scenario_player_2]
            print("Scenario is " + self.scenarios[self.scenario_players[0]])
            self.end_turn_btn.text = str(self.scenarios[self.scenario_players[0]])

            self.scenario_counter = 0
            if not lhp:
                self.player1.units[0].hp = 20
            if not rhp:
                self.player2.units[0].hp = 20

            self.skynet1.set_param(x, y, enx, eny)
            self.skynet2.set_param(enx, eny, x, y)
            self.skynets = [self.skynet1, self.skynet2]

        if GAMEMODE == SKYNET_VS_P:
            x, y = self.get_random_pos()
            enx, eny = self.get_random_pos(x, y)
            self.map.reset(x, y, enx, eny)
            self.scenario_player_1, self.scenario_player_2, lhp, rhp, = self.get_random_scenario()
            print("Scenario is " + self.scenarios[self.scenario_player_2] + " from Skynet's point of view")
            self.scenario_counter = 0
            if not lhp:
                self.player1.units[0].hp = 20
            if not rhp:
                self.player2.units[0].hp = 20
            self.skynet.set_param(enx, eny, x, y)
            self.new_turn()

    def quit(self):
        pg.quit()
        sys.exit()

    def erase_highlights(self):  # this is currently only used to remove the highlight, usually we'd move pieces around here
        # but we do that in Map when we need to because our game is not in real-time
        # update portion of the game loop
        # self.unit_sprites.update()
        self.foreground_sprites.update()

    def draw_grid(self):  # draws line in a grid
        # stops at 32 width to leave space for text and buttons. More than that, we need to change screen size
        for x in range(0, GRID_WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, GRID_HEIGHT))
        for y in range(0, GRID_HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (GRID_WIDTH, y))

    def draw(self):  # draw everything from bottom to top layer
        # we might have to split the draw functions between the text files and the game map later on
        if NO_DRAW:
            return
        # if GAMEMODE == AI:
        #     self.map.highlight_tile(self.goal_pos[0], self.goal_pos[1])
        self.screen.fill(BGCOLOR)
        self.terrain_sprites.draw(self.screen)
        self.unit_sprites.draw(self.screen)
        self.foreground_sprites.draw(self.screen)

        self.available_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            button.draw()
        for box in self.textboxes:
            box.draw()
        pg.display.flip()
        time.sleep(WAIT_TIME)

    def events(self):
        # catch all events here
        self.end_turn_btn.text = "End Turn"
        if GAMEMODE == SKYNET_VS_SKYNET or GAMEMODE == SKYNET_VS_AI:
            self.end_turn_btn.text = self.scenarios[self.scenario_player_1]
        self.cancel_btn.text = ""
        self.attack_btn.text = ""
        self.special_btn.text = ""
        if GAMEMODE == SKYNET_VS_AI:
            if SCENARIO == ATTACK:
                if self.iterative_training:
                    self.iterative_attack_training()
                    self.reset()
                else:
                    self.interpret_ai()
            else:
                self.interpret_ai()
            for event in pg.event.get():
                if event.type == pg.QUIT:  # allow close game
                    self.quit()
        elif GAMEMODE == SKYNET_VS_SKYNET:
            self.ask_interpret_skynet_vs_skynet()
            for event in pg.event.get():
                if event.type == pg.QUIT:  # allow close game
                    self.quit()
        elif GAMEMODE == SKYNET_VS_P:
            for event in pg.event.get():
                if event.type == pg.QUIT:  # allow close game
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                if event.type == pg.MOUSEBUTTONDOWN:  # enters when the user click on something
                    x, y = self.get_grid_coord()  # gets the grid coord of where the user clicked in grid x and y
                    if x > GRID_X_SIZE - 1 or y > GRID_Y_SIZE - 1:
                        # if x or y > GRID_X/Y_SIZE-1, that means the user didn't click the map but clicked the buttons or text box instead
                        # we need to get the position again but this time in pixel.
                        x, y = pg.mouse.get_pos()
                        for button in self.buttons_list:  # checks if any button created are being hovered before clicking
                            if button.isOver(x, y):
                                if button == self.end_turn_btn:
                                    self.new_turn()
                                    self.scenario_counter += 1
                                    self.draw()
                                    if not self.player1.units or not self.player2.units:
                                        self.reset()
                                        return
                                    else:
                                        self.ask_interpret_skynet()
                                        self.scenario_counter += 1
                                        self.draw()
                                        if self.scenario_counter == MAX_SCENARIO_TURN:
                                            print("Ended on scenario turn " + str(MAX_SCENARIO_TURN))
                                            self.reset()
                                            return
                                        elif not self.player1.units or not self.player2.units:
                                            self.reset()
                                            return
                                        else:
                                            self.new_turn()
                    else:
                        self.tile_selected(x, y)  # Function takes care of actions when selecting a tile
        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:  # allow close game
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                if event.type == pg.MOUSEBUTTONDOWN:  # enters when the user click on something
                    x, y = self.get_grid_coord()  # gets the grid coord of where the user clicked in grid x and y
                    if x > GRID_X_SIZE - 1 or y > GRID_Y_SIZE - 1:
                        # if x or y > GRID_X/Y_SIZE-1, that means the user didn't click the map but clicked the buttons or text box instead
                        # we need to get the position again but this time in pixel.
                        x, y = pg.mouse.get_pos()
                        for button in self.buttons_list:  # checks if any button created are being hovered before clicking
                            if button.isOver(x, y):
                                if button == self.end_turn_btn:
                                    self.new_turn()
                    else:
                        self.tile_selected(x, y)  # Function takes care of actions when selecting a tile

    def get_grid_coord(self):  # returns the position of the mouse in grid x and y rather than in pixels
        x, y = pg.mouse.get_pos()
        x = math.floor(x / TILESIZE)  # Divide by tile size and floor it to get the tile coord,
        y = math.floor(y / TILESIZE)  # almost everything works in map coordinate except the buttons
        return x, y

    def print_details(self, x, y):  # This prints information on the text boxes, pulls data from map
        if self.map.is_unit(x, y):
            self.print_unit_details(x, y)
        else:
            self.unit_text.text.clear()
        self.print_terrain_details(x, y)

    def tile_selected(self, x, y):  # Function takes care of actions when selecting tile
        # x, y are the current position while x2, y2 are the new position.
        unit_selected = False
        self.erase_highlights()
        self.print_details(x, y)
        if self.map.get_terrain(x, y).name == "factory":
            # This is a chain of if that checks if the tile is a factory and it is own by the player clicking on it.
            # Since only BUILDING type terrain have owners, I have to do a chain of if to avoid an error. We need to improve this
            # Solution: Make all terrain class the same (master class in terrain file)
            # TODO Fix this
            if self.map.get_terrain(x, y).owner:
                if self.map.get_terrain(x, y).owner.ID == self.turn:
                    #  if you own the factory but have a unit over it, priority goes to the unit, so the unit is selected
                    if self.map.is_unit(x, y):
                        unit_selected = True
                    #  Otherwise, we select the factory and use the factory function
                    else:
                        self.factory(x, y)
        #  if the tile selected has a unit on it, enters
        if self.map.is_unit(x, y) or unit_selected is True:
            unit = self.map.get_unit(x, y)
            if unit.player.ID == self.turn:  # check if the unit is owned by the player
                if unit.available:  # check if the unit is available (in general, if it hasn't moved yet)
                    unit.highlight()  # This highlight the unit that is currently selected
                    acted, show_options, x2, y2, fuel_cost = self.move_unit(x, y)
                    if show_options:  # if the unit moved, it can proceed to attack another unit in range or other actions
                        acted = self.options(x, y, x2, y2, acted)  # This function takes care of all attacking/action shenanigans
                    if acted:  # if the unit attacked or used a turn ending action, we calculate the fuel lost and remove the unit from available unit.
                        unit.fuel -= unit.movement - fuel_cost  # how fuel is calculated is explained in highlight
                        unit.end_turn()
                    else:
                        unit.unhighlight()  # This removes the selected_unit highlight and replaces it with available_unit highlight()
                    self.erase_highlights()
            else:  # in case the user select a tile with no unit or an enemy unit, it will show enemy attack range
                if unit.can_attack:
                    if unit.type == ARTILLERY or unit.type == MISSILES or unit.type == ROCKETS:  # These unit have indirect attack so they highlight differently
                        self.indirect_atk_highlight(x, y)
                    else:
                        self.highlight_enemy(self.map.get_unit_mvt_type(x, y), self.map.get_mvt(x, y),
                                             self.map.get_unit(x, y).fuel, x, y)

    def move_unit(self, x, y):
        # This function takes care of everything related to moving a unit.
        # it takes the x and y of the unit selected, highlight the tile where the unit can move
        # returns
        self.highlight(self.map.get_unit_mvt_type(x, y), self.map.get_mvt(x, y), self.map.get_unit(x, y).fuel, x,
                       y)  # Highlights the valid tiles that can be moved onto
        self.end_turn_btn.text = "End Mvt"
        self.cancel_btn.text = "Cancel"
        self.draw()  # draws the highlight
        fuel_cost = self.map.get_unit(x, y).movement  # fuel cost is explained in highlight()
        position_confirmed = False  # Value tells us the location and move have been confirmed
        position_selected = False  # Value tells us when a position on the grid has been selected
        show_options = False  # return value to indicate if we need to show options after moving
        moved = False  # return value that indicates if a unit moved
        while not position_confirmed:  # loops until the user clicks a tile
            event = pg.event.wait()
            if event.type == pg.MOUSEBUTTONDOWN:  # enters when the user clicks on tile
                x2, y2 = self.get_grid_coord()  # Coordinate of the new tile clicked
                if x2 > GRID_X_SIZE - 1 or y2 > GRID_Y_SIZE - 1:  # if x > GRID_X_SIZE-1, the user clicked the buttons of a textbox
                    x2, y2 = pg.mouse.get_pos()  # gets the position again but this time in pixel.
                    if self.cancel_btn.isOver(x2,
                                              y2):  # Cancel the move order, currently doesn't really do anything but might change later on
                        fuel_cost = self.map.get_unit(x,
                                                      y).movement  # return fuel cost will be the unit movement, when calculating, it will cost the unit 0 fuel
                        show_options = False
                        moved = False
                        position_confirmed = True
                    elif self.end_turn_btn.isOver(x2, y2):
                        show_options = False
                        moved = True
                        position_confirmed = True
                    elif self.special_btn.isOver(x2, y2) and position_selected and self.special_btn.text == "Merge":
                        # TODO I just realized merging transport might be a problem if they have unit inside,
                        #  idk what happens in the game but we will have to look into it
                        show_options = False
                        moved = True
                        position_confirmed = True
                        self.merge_unit(x, y, position_selected[0], position_selected[1])
                    elif self.special_btn.isOver(x2, y2) and position_selected and self.special_btn.text == "Embark":
                        show_options = False
                        moved = True
                        position_confirmed = True
                        self.embark_unit(x, y, position_selected[0], position_selected[1])
                elif self.map.is_highlight(x2, y2) and not self.map.is_unit(x2, y2):
                    # if the tile has a highlight and no unit on it, it is valid and the unit moves
                    self.map.move_unit(x, y, x2, y2)  # moves the unit, Map takes care of it
                    fuel_cost = self.map.get_tile(x2, y2).fuel_cost  # fuel cost explained in highlight()
                    position_selected = False
                    self.special_btn.text = ""
                    self.preview_text.text.clear()
                    self.draw()
                    moved = True
                    show_options = True
                    position_confirmed = True
                    self.print_details(x2, y2)
                elif self.map.is_unit(x2, y2) and self.map.is_highlight(x2, y2):  # Stay on the same tile or Merge 2 units
                    unit1 = self.map.get_unit(x, y)
                    unit2 = self.map.get_unit(x2, y2)
                    if x == x2 and y == y2:  # Stay on the same tile
                        self.special_btn.text = ""
                        moved = False
                        show_options = True
                        position_confirmed = True
                        fuel_cost = unit1.movement
                    elif self.turn == unit2.player.ID and unit1.type == unit2.type and unit2.hp != FULL_HP:  # Merge with another unit
                        position_selected = (x2, y2)
                        fuel_cost = self.map.get_tile(x2, y2).fuel_cost
                        self.special_btn.text = "Merge"
                        self.print_merge_preview(x, y, x2, y2)
                        self.print_details(x2, y2)
                        self.draw()
                    elif self.turn == unit2.player.ID and unit2.type == APC and not unit2.holding and (
                            unit1.type == INFANTRY or unit1.type == MECH):  # If the unit is a transport and does not contains a unit, can embark
                        position_selected = (x2, y2)
                        self.special_btn.text = "Embark"
                        fuel_cost = self.map.get_tile(x2, y2).fuel_cost
                        self.print_details(x2, y2)
                        self.draw()
                else:
                    self.print_details(x2, y2)
                    self.draw()
        self.erase_highlights()
        return moved, show_options, x2, y2, fuel_cost
        # x2,y2 are the x and y of the new position of the unit.

    def highlight(self, mvt_type, mvt, fuel, x, y, direction="None"):
        # This function takes care of highlighting tiles of available movement for a unit
        # It is a recurring function that stops once an impassable terrain is reached or the max movement is reached or fuel runs out
        # It takes the unit mvt type (there are 7 in the game), the unit mvt (how much it can move) and x and y and fuel remaining
        # TODO Feel free to optimise this function!

        if mvt == -1 or fuel < 0 or x < 0 or x > GRID_X_SIZE - 1 or y < 0 or y > GRID_Y_SIZE - 1:  # if out of movement or out of the game grid, stop
            return

        if not self.map.get_tile_mvt_cost(mvt_type, x, y):
            return
            # enters if the terrain is impassable for the given unit and stop. We know it is impassable because the
            # mvt cost for a given type will be 0 if the unit can't go there.
            # (ex tank in water, tank mvt_type is TREAD, river tread_mvt_cost = 0)

        if self.map.is_unit(x, y):
            if self.map.get_unit(x, y).player.ID != self.turn:
                return
                # enters if the tile has an enemy unit on it

        self.map.highlight_tile(x, y)
        if self.map.get_tile(x, y).fuel_cost < mvt:
            self.map.get_tile(x, y).fuel_cost = mvt
        # if nothing is in the way, we highlight the tile as a tile the unit can move onto,
        # we also modify the fuel cost of the tile to the current movement remaining for the unit.

        # Here's how fuel works: while highlighting, the remaining movement left goes down. For example, tank has 6 movement.
        # While highlighting, we go through a forest and lose 4 fuel. 2 Fuel is left. While highlighting this tile, we store this
        # value in the tile. We keep iterating, it's possible to go around the forest and and up on the same tile but only using
        # 3 fuel this time with 3 fuel remaining. This higher fuel remaining takes over the previous 2 fuel remaining on the tile fuel cost.
        # When the user selects the tile he want the unit to move onto, we check the fuel_cost of the tile and compare
        # it to the movement of the unit. In our example Tile.fuel_cost=3 and Tank.mvt = 6. 6-3=3, the tank used 3 fuel and
        # we substract that to his remaining fuel. (This is done in tile_selected()) This method guarantees the optimal path (least fuel used) is always prioritized
        # and makes it possible to calculate fuel because I couldn't come up with another way to do this without rewriting a lot
        # of code. The Tile fuel_cost is set to 0 when we remove all the highlights after moving.
        # Feel free to find a better way to do this

        # This is where the function loops on itself, it goes in all 4 directions to check for potential valid tiles
        # With each iteration, the movement left and fuel left go down, if any run out, we stop.
        # to save some iterations, it doesn't go back the way it just came. AKA if it's going upwards, it won't go back
        # down immediately but, it might can go up, left, down and right and check the same tile again.
        # This can be improved (fuel calculation depends on this feature though)

        if direction != "down":
            if y - 1 >= 0:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x, y - 1)
                if mvt - mvt_cost > -1 and fuel - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight(mvt_type, mvt - mvt_cost, fuel - mvt_cost, x, y - 1, "up")  # going up
        if direction != "right":
            if x - 1 >= 0:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x - 1, y)
                if mvt - mvt_cost > -1 and fuel - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight(mvt_type, mvt - mvt_cost, fuel - mvt_cost, x - 1, y, "left")  # going left
        if direction != "left":
            if x + 1 <= GRID_X_SIZE - 1:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x + 1, y)
                if mvt - mvt_cost > -1 and fuel - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight(mvt_type, mvt - mvt_cost, fuel - mvt_cost, x + 1, y, "right")  # going right
        if direction != "up":
            if y + 1 <= GRID_Y_SIZE - 1:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x, y + 1)
                if mvt - mvt_cost > -1 and fuel - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight(mvt_type, mvt - mvt_cost, fuel - mvt_cost, x, y + 1, "down")  # going down

    def highlight_enemy(self, mvt_type, mvt, fuel, x, y, direction="None"):
        # Same function as highlight but modified. This one highlight where an enemy unit can attack and works a bit differently

        if x < 0 or x > GRID_X_SIZE - 1 or y < 0 or y > GRID_Y_SIZE - 1:  # if out of movement or out of the game grid, stop
            return

        if not self.map.get_tile_mvt_cost(mvt_type, x, y):
            self.map.atk_highlight_tile(x, y)
            return

        if self.map.is_unit(x, y):
            if self.map.get_unit(x, y).player.ID == self.turn:
                self.map.atk_highlight_tile(x, y)
                return

        self.map.atk_highlight_tile(x, y)
        if mvt < 1 or not self.map.get_tile_mvt_cost(mvt_type, x, y):
            self.direct_atk_highlight(x, y)
            return

        # This is where the function loops on itself, it goes in all 4 directions to check for potential valid tiles
        # to save some iterations, it doesn't go back the way it just came. AKA if it's going upwards, it won't go back
        # down immediately but, it might can go up, left, down and right and check the same tile again.
        # This can be improved

        if direction != "down":
            if y - 1 >= 0:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x, y - 1)
                if mvt - mvt_cost > -1 and fuel - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight_enemy(mvt_type, mvt - mvt_cost, fuel - mvt_cost, x, y - 1, "up")  # going up
                else:
                    self.direct_atk_highlight(x, y)
        if direction != "right":
            if x - 1 >= 0:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x - 1, y)
                if mvt - mvt_cost > -1 and fuel - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight_enemy(mvt_type, mvt - mvt_cost, fuel - mvt_cost, x - 1, y, "left")  # going left
                else:
                    self.direct_atk_highlight(x, y)
        if direction != "left":
            if x + 1 <= GRID_X_SIZE - 1:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x + 1, y)
                if mvt - mvt_cost > -1 and fuel - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight_enemy(mvt_type, mvt - mvt_cost, fuel - mvt_cost, x + 1, y, "right")  # going right
                else:
                    self.direct_atk_highlight(x, y)
        if direction != "up":
            if y + 1 <= GRID_Y_SIZE - 1:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x, y + 1)
                if mvt - mvt_cost > -1 and fuel - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight_enemy(mvt_type, mvt - mvt_cost, fuel - mvt_cost, x, y + 1, "down")  # going down
                else:
                    self.direct_atk_highlight(x, y)

    def highlight_drop(self, x, y):
        # This highlights tiles where a unit can be dropped onto from transport
        unit = self.map.get_unit(x, y)
        drop = unit.holding
        mvt_type = drop.mvt_type
        if y - 1 >= 0:
            if self.map.get_tile_mvt_cost(mvt_type, x, y - 1) != 0 and not self.map.is_unit(x, y - 1):
                self.map.highlight_tile(x, y - 1)  # up
        if x - 1 >= 0:
            if self.map.get_tile_mvt_cost(mvt_type, x - 1, y) != 0 and not self.map.is_unit(x - 1, y):
                self.map.highlight_tile(x - 1, y)  # left
        if x + 1 <= GRID_X_SIZE - 1:
            if self.map.get_tile_mvt_cost(mvt_type, x + 1, y) != 0 and not self.map.is_unit(x + 1, y):
                self.map.highlight_tile(x + 1, y)  # right
        if y + 1 <= GRID_Y_SIZE - 1:
            if self.map.get_tile_mvt_cost(mvt_type, x, y + 1) != 0 and not self.map.is_unit(x, y + 1):
                self.map.highlight_tile(x, y + 1)  # down

    def factory(self, x1, y1):
        # This function is mostly visual shenanigans to show the user his options with the factory.
        owner = self.map.get_terrain(x1, y1).owner
        self.attack_btn.text = "Prev"
        self.special_btn.text = "Next"
        self.end_turn_btn.text = "Confirm"
        self.cancel_btn.text = "Cancel"
        confirmed = False
        selected_unit_name, selected_unit_symbol = self.print_factory_preview(None, owner)
        iterator = None
        self.draw()
        while not confirmed:  # loops until the user cancels or confirms
            event = pg.event.wait()
            if event.type == pg.MOUSEBUTTONDOWN:  # enters when the user clicks on tile
                x, y = pg.mouse.get_pos()
                if self.cancel_btn.isOver(x, y):
                    confirmed = True
                elif self.end_turn_btn.isOver(x, y) and selected_unit_symbol != '.':
                    if owner.funds > unit_costs[selected_unit_name]:
                        confirmed = True
                        self.map.get_tile(x1, y1).add_unit(owner, selected_unit_symbol)
                        owner.funds -= unit_costs[selected_unit_name]
                    else:
                        iterator = None
                        selected_unit_name = None
                        selected_unit_symbol = '.'
                        self.preview_text.text.clear()
                        text = "You don't have enough funds for this unit"
                        self.preview_text.text.append(text)

                elif self.attack_btn.isOver(x, y):
                    if iterator is None:
                        iterator = 9
                    else:
                        iterator -= 1
                        if iterator < 0:
                            iterator = 9
                    selected_unit_name, selected_unit_symbol = self.print_factory_preview(iterator, owner)
                elif self.special_btn.isOver(x, y):
                    if iterator is None:
                        iterator = 0
                    else:
                        iterator += 1
                        if iterator > 9:
                            iterator = 0
                    selected_unit_name, selected_unit_symbol = self.print_factory_preview(iterator, owner)
            self.draw()

    def options(self, old_x, old_y, x, y, moved):
        # This function takes care of handling everything related to attacking and other possible actions.
        # It highlights the tiles that can be attacked and attack the corresponding
        # If we want to cancel everything, we need to move it back to it's original spot and we need the old_x and old_y for that
        if self.map.get_unit(x, y).can_attack:
            if (self.map.get_unit(x, y).type == ARTILLERY or self.map.get_unit(x, y).type == MISSILES or self.map.get_unit(x,
                                                                                                                           y).type == ROCKETS) and not moved:
                # if the unit is an indirect attacker, it can't move and attack on the same turn so we check if it moved before allowing it to attack
                self.indirect_atk_enemy_highlight(x, y)  # Highlights tiles that can be attacked by indirect attackers
            else:
                self.direct_atk_enemy_highlight(x, y)
        if self.map.get_unit(x, y).type == APC:
            # if the unit is an APC, it can refuel units
            self.attack_btn.text = "Refuel"
            if self.map.get_unit(x, y).holding:
                # if it's holding a unit, it can drop it
                self.special_btn.text = "Drop"
        self.draw()
        acted = False  # Value determines if the unit did something
        target_confirmed = False  # value determines if the target for an attack or other actions has been confirmed
        target_selected = False  # value determines if the target for an attack or other actions has been selected
        while not target_confirmed:  # loops until the user clicks a tile
            event = pg.event.wait()
            if event.type == pg.MOUSEBUTTONDOWN:  # enters when the user clicks on tile or button
                x2, y2 = self.get_grid_coord()
                if x2 > GRID_X_SIZE - 1 or y2 > GRID_Y_SIZE - 1:
                    x2, y2 = pg.mouse.get_pos()
                    if self.cancel_btn.isOver(x2, y2):  # Cancel everything
                        target_confirmed = True
                        self.map.move_unit(x, y, old_x, old_y)  # Moves unit back if the user cancels
                        acted = False
                    elif self.end_turn_btn.isOver(x2, y2):  # end the movement of a unit
                        target_confirmed = True
                        acted = True
                    elif self.attack_btn.isOver(x2,
                                                y2) and target_selected and self.attack_btn.text == "Confirm Atk":  # Confirm an attack
                        self.atk_target(x, y, target_selected[0], target_selected[1])
                        target_confirmed = True
                        self.draw()
                        acted = True
                    elif self.special_btn.isOver(x2,
                                                 y2) and target_selected and self.special_btn.text == "Capture":  # Confirm the capture of a building
                        self.capture_building(x, y)
                        target_confirmed = True
                        acted = True
                    elif self.special_btn.isOver(x2,
                                                 y2) and self.special_btn.text == "Drop":  # initiate the drop action for an APC
                        self.special_btn.text = "Confirm Drop"
                        self.highlight_drop(x, y)
                        self.draw()
                    elif self.special_btn.isOver(x2,
                                                 y2) and target_selected and self.special_btn.text == "Confirm Drop":  # Confirm the drop action for an APC
                        self.special_btn.text = ""
                        self.drop_unit(x, y, target_selected[0], target_selected[1])
                        target_confirmed = True
                        acted = True
                    elif self.attack_btn.isOver(x2,
                                                y2) and self.attack_btn.text == "Refuel":  # Confirm the refuel action for an APC
                        self.attack_btn.text = ""
                        self.refuel(x, y)
                        target_confirmed = True
                        acted = True
                elif self.map.is_atk_highlight(x2,
                                               y2):  # if the tiles selected has a valid target, initiate the attack preview and confirmation
                    self.print_details(x2, y2)
                    # if self.map.get_unit(x, y).can_attack:
                    self.print_atk_preview(x, y, x2, y2)
                    self.attack_btn.text = "Confirm Atk"
                    target_selected = (x2, y2)
                    self.draw()
                elif self.map.is_highlight(x2, y2):  # if the tile selected has been highlighted (for drop in general)
                    self.print_details(x2, y2)
                    target_selected = (x2, y2)
                    self.draw()
                elif self.map.get_terrain(x2, y2).type == BUILDING and x2 == x and y2 == y and \
                        (self.map.get_unit(x, y).type == INFANTRY or self.map.get_unit(x,
                                                                                       y).type == MECH):  # if the tile selected is a building, can capture possibly
                    if not self.map.get_terrain(x2, y2).owner:  # TODO find better way to do this
                        self.special_btn.text = "Capture"
                        self.draw()
                        target_selected = True
                    elif self.map.get_terrain(x2, y2).owner.ID != self.turn:
                        self.special_btn.text = "Capture"
                        self.draw()
                        target_selected = True
                else:  # catch all if, the tile selected isn't something that allows an interaction with the unit
                    target_selected = False
                    if self.attack_btn.text != "Refuel":
                        self.attack_btn.text = ""
                    if self.special_btn.text != "Confirm Drop" and self.special_btn.text != "Confirm Attack":
                        self.special_btn.text = ""
                    self.preview_text.text.clear()
                    self.print_details(x2, y2)
                    self.draw()
        return acted

    def direct_atk_highlight(self, x, y):
        # highlight tile that can be attacked
        # only direct attacks. Used by highlight_enemy to highlight where an enemy unit can attack after moving, etc.
        if y - 1 >= 0:
            self.map.atk_highlight_tile(x, y - 1)  # up
        if x - 1 >= 0:
            self.map.atk_highlight_tile(x - 1, y)  # left
        if x + 1 <= GRID_X_SIZE - 1:
            self.map.atk_highlight_tile(x + 1, y)  # right
        if y + 1 <= GRID_Y_SIZE - 1:
            self.map.atk_highlight_tile(x, y + 1)  # down

    def indirect_atk_highlight(self, x, y):
        # Indirect attack highlight for enemy unit
        _range = self.map.get_unit(x, y).range
        range_max = _range[1]
        range_min = _range[0] - 1
        for dy in range(y - range_max, y + range_max + 1):
            for dx in range(x - range_max + (abs(y - dy)), x + range_max - (abs(y - dy)) + 1):
                if dx == x and dy == y:
                    pass
                elif 0 <= dy <= GRID_Y_SIZE - 1 and 0 <= dx <= GRID_X_SIZE - 1:
                    self.map.atk_highlight_tile(dx, dy)
        for dy in range(y - range_min, y + range_min + 1):
            for dx in range(x - range_min + (abs(y - dy)), x + range_min - (abs(y - dy)) + 1):
                if dx == x and dy == y:
                    pass
                elif 0 <= dy <= GRID_Y_SIZE - 1 and 0 <= dx <= GRID_X_SIZE - 1:
                    if self.map.is_atk_highlight(dx, dy):
                        self.map.atk_unhighlight_tile(dx, dy)

    def direct_atk_enemy_highlight(self, x, y):
        # highlight tile that can be attacked
        # only direct attacks, similar to direct_atk_highlight but this one checks if the attacking unit is allowed to attack the other unit before highlighting
        # For example, infantry can't attack bomber
        unit = self.map.get_unit(x, y)

        if y - 1 >= 0:
            if self.map.is_unit(x, y - 1):
                if self.can_attack(unit, x, y - 1) and self.map.get_unit(x, y - 1).player.ID != self.turn:
                    self.map.atk_highlight_tile(x, y - 1)  # up
        if x - 1 >= 0:
            if self.map.is_unit(x - 1, y):
                if self.can_attack(unit, x - 1, y) and self.map.get_unit(x - 1, y).player.ID != self.turn:
                    self.map.atk_highlight_tile(x - 1, y)  # left
        if x + 1 <= GRID_X_SIZE - 1:
            if self.map.is_unit(x + 1, y):
                if self.can_attack(unit, x + 1, y) and self.map.get_unit(x + 1, y).player.ID != self.turn:
                    self.map.atk_highlight_tile(x + 1, y)  # right
        if y + 1 <= GRID_Y_SIZE - 1:
            if self.map.is_unit(x, y + 1):
                if self.can_attack(unit, x, y + 1) and self.map.get_unit(x, y + 1).player.ID != self.turn:
                    self.map.atk_highlight_tile(x, y + 1)  # down

    def indirect_atk_enemy_highlight(self, x, y):
        # Indirect attack highlight for enemy unit
        # similar to indirect_atk_highlight but this one checks if the attacking unit is allowed to attack the other unit before highlighting
        # For example, artillery can't attack bomber
        unit = self.map.get_unit(x, y)
        _range = unit.range
        range_max = _range[1]
        range_min = _range[0] - 1
        for dy in range(y - range_max, y + range_max + 1):
            for dx in range(x - range_max + (abs(y - dy)), x + range_max - (abs(y - dy)) + 1):
                if dx == x and dy == y:
                    pass
                elif 0 <= dy <= GRID_Y_SIZE - 1 and 0 <= dx <= GRID_X_SIZE - 1:
                    if self.map.is_unit(dx, dy):
                        if self.can_attack(unit, dx, dy) and self.map.get_unit(dx, dy).player.ID != self.turn:
                            self.map.atk_highlight_tile(dx, dy)
        for dy in range(y - range_min, y + range_min + 1):
            for dx in range(x - range_min + (abs(y - dy)), x + range_min - (abs(y - dy)) + 1):
                if dx == x and dy == y:
                    pass
                elif 0 <= dy <= GRID_Y_SIZE - 1 and 0 <= dx <= GRID_X_SIZE - 1:
                    if self.map.is_atk_highlight(dx, dy):
                        self.map.atk_unhighlight_tile(dx, dy)

    def can_attack(self, attacker, x, y):  # Check if the attacker can attack the other unit
        defender = self.map.get_unit(x, y)
        if attacker.ammo and main_wpn[defender.type][attacker.type]:
            return True
        elif alt_wpn[defender.type][attacker.type]:
            return True
        else:
            return False

    def capture_building(self, x, y):  # Capture a building
        unit = self.map.get_unit(x, y)
        terrain = self.map.get_terrain(x, y)

        damage = math.ceil(unit.hp / 10)
        terrain.hp -= damage
        if terrain.hp < 1:
            terrain.hp = 20
            self.map.capture(x, y, unit.player)

    def atk_target(self, x, y, x2, y2, counter=True):
        # this function takes care of damage calculation and updating the corresponding hp
        attacker = self.map.get_unit(x, y)
        defender = self.map.get_unit(x2, y2)
        defender_def = self.map.get_defense(x2, y2)

        if not attacker.can_attack:
            return
        if attacker.type == ARTILLERY or defender.type == ARTILLERY:  # if the attack is indirect, there won't be a counter attack from the defender
            counter = False

        if attacker.ammo:
            # this checks which weapon is strongest (main or alt) against the target and if ammo is left
            # for example, the mech will use it's alt weapon against infantry but will use rockets against tanks, if no ammo is left,
            # it will default to alt weapon. Damage changes accordingly
            main_wpn_dmg = main_wpn[defender.type][attacker.type]
            alt_wpn_dmg = alt_wpn[defender.type][attacker.type]
            if main_wpn_dmg > alt_wpn_dmg:
                base_dmg = main_wpn_dmg
                weapon_used = MAIN
            else:
                base_dmg = alt_wpn_dmg
                weapon_used = ALT
        else:
            alt_wpn_dmg = alt_wpn[defender.type][attacker.type]
            base_dmg = alt_wpn_dmg
            weapon_used = ALT

        # This is the damage formula from the actual game
        terrain_mod = 1 - (defender_def * defender.hp/10)/100
        attacker_mod = attacker.hp / 100
        final_dmg = base_dmg * terrain_mod * attacker_mod

        final_dmg = round(final_dmg)
        defender.hp -= final_dmg
        if defender.hp < 1:
            self.map.remove_unit(x2, y2)
            counter = False
        if weapon_used == MAIN:
            attacker.ammo -= 1

        self.preview_text.text.clear()
        text = "You dealt " + str(final_dmg) + " damage"
        self.preview_text.text.append(text)
        if counter:
            self.atk_target(x2, y2, x, y, False)

    def merge_unit(self, x, y, x2, y2):  # Merge unit function
        unit1 = self.map.get_unit(x, y)
        unit2 = self.map.get_unit(x2, y2)
        unit1_hp = unit1.hp
        self.map.remove_unit(x, y)
        unit2.hp += unit1_hp
        unit2.end_turn()
        if unit2.hp > FULL_HP:
            excess = unit2.hp - FULL_HP
            # TODO add fund depending on excess hp
            unit2.hp = FULL_HP

    def embark_unit(self, x, y, x2, y2):  # Embark unit function
        unit1 = self.map.get_unit(x, y)
        unit2 = self.map.get_unit(x2, y2)
        unit2.holding = unit1
        self.map.embark_unit(x, y)

    def drop_unit(self, x, y, x2, y2):  # drop unit function
        dropper = self.map.get_unit(x, y)
        unit = dropper.holding
        self.map.drop_unit(x2, y2, unit)
        dropper.holding = None

    def refuel(self, x, y):  # Refuel surrounding unit function
        # TODO the refuel function also refuels enemy units.....
        if y - 1 >= 0:
            if self.map.is_unit(x, y - 1):
                self.map.get_unit(x, y - 1).refuel()
        if x - 1 >= 0:
            if self.map.is_unit(x - 1, y):
                self.map.get_unit(x - 1, y).refuel()
        if x + 1 <= GRID_X_SIZE - 1:
            if self.map.is_unit(x + 1, y):
                self.map.get_unit(x + 1, y).refuel()
        if y + 1 <= GRID_Y_SIZE - 1:
            if self.map.is_unit(x, y + 1):
                self.map.get_unit(x, y + 1).refuel()

    def new_turn(self):
        # Called at the end of every turn, adds funds from building, does repairs from unit on friendly building, etc.
        # Unhighlight units of the player ending his turn and highlight available unit for the player whose turn is starting
        # TODO implement the fuel cost at the end of turn for air and sea unit
        self.erase_highlights()
        self.preview_text.text.clear()
        for player in self.players:
            if self.turn == player.ID:
                for unit in player.units:
                    died = unit.end_turn()
                    if died:
                        self.map.remove_unit(unit.x, unit.y)
            else:
                for unit in player.units:
                    unit.new_turn()
                for city in player.buildings:
                    city.add_funds()
                    self.map.building_refuel(city.x, city.y)

        self.turn = (self.turn + 1) % NB_PLAYER
        self.turn_counter += 1
        global NO_DRAW
        if NO_DRAW is False and GAMEMODE == SKYNET_VS_AI and self.turn_counter % STOP_DRAW_AT == 0:
            NO_DRAW = True
        # if GAMEMODE == AI_VS_AI and self.turn_counter == 3:
        #     self.iteration += 1
        #     if not NO_DRAW:
        #         self.draw()
        #     self.erase_highlights()
        #     self.reset()
        # TODO this is a temporary fix when we want to run games with only one player
        if NB_PLAYER == 1:
            for player in self.players:
                for unit in player.units:
                    unit.new_turn()

    def print_unit_details(self, x, y):
        # pretty much just takes info from the unit class and appends them to the textbox text list to print
        # this will have to be improved, it was hella late when I coded this and didn't put too much thought into it
        unit = self.map.get_unit(x, y)

        self.unit_text.text.clear()
        text = "Type: " + unit.name
        self.unit_text.text.append(text)
        if unit.mvt_type == INFANTRY:
            text = "Mvt type: " + "Infantry"
        elif unit.mvt_type == TREAD:
            text = "Mvt type: " + "Tread"
        elif unit.mvt_type == TIRES:
            text = "Mvt type: " + "Tires"
        elif unit.mvt_type == MECH:
            text = "Mvt type: " + "Mech"
        elif unit.mvt_type == AIR:
            text = "Mvt type: " + "Air"
        elif unit.mvt_type == TRANSPORT:
            text = "Mvt type: " + "Transport"
        elif unit.mvt_type == SHIP:
            text = "Mvt type: " + "Ship"
        self.unit_text.text.append(text)
        text = "Mvt: " + str(unit.movement)
        self.unit_text.text.append(text)
        text = "HP: " + str(math.ceil(unit.hp / 10))
        self.unit_text.text.append(text)
        if unit.player.ID == PLAYER1:
            text = "Player: Red"
        elif unit.player.ID == PLAYER2:
            text = "Player: Blue"
        self.unit_text.text.append(text)
        text = "Ammo left: " + str(unit.ammo)
        self.unit_text.text.append(text)
        text = "Fuel left: " + str(unit.fuel)
        self.unit_text.text.append(text)
        if unit.type == ARTILLERY:
            _range = unit.range
            text = "Range: " + str(_range[0]) + ", " + str(_range[1])
            self.unit_text.text.append(text)

    def print_terrain_details(self, x, y):
        # pretty much just takes info from the terrain class and appends them to the textbox text list to print
        # this will have to be improved, it was hella late when I coded this and didn't put too much thought into it
        self.terrain_text.text.clear()
        text = "Type: " + self.map.get_terrain_name(x, y)
        self.terrain_text.text.append(text)

        text = "Infantry cost: " + str(self.map.get_tile_mvt_cost(INFANTRY, x, y))
        self.terrain_text.text.append(text)

        text = "Mech cost: " + str(self.map.get_tile_mvt_cost(MECH, x, y))
        self.terrain_text.text.append(text)

        text = "Tires cost: " + str(self.map.get_tile_mvt_cost(TIRES, x, y))
        self.terrain_text.text.append(text)

        text = "Tread cost: " + str(self.map.get_tile_mvt_cost(TREAD, x, y))
        self.terrain_text.text.append(text)

        text = "Air cost: " + str(self.map.get_tile_mvt_cost(AIR, x, y))
        self.terrain_text.text.append(text)

        text = "Ship cost: " + str(self.map.get_tile_mvt_cost(SHIP, x, y))
        self.terrain_text.text.append(text)

        text = "Transport cost: " + str(self.map.get_tile_mvt_cost(TRANSPORT, x, y))
        self.terrain_text.text.append(text)

        text = "Defense: " + str(self.map.get_defense(x, y))
        self.terrain_text.text.append(text)

        if self.map.get_terrain(x, y).type == BUILDING:  # If the terrain type is a building, if also prints the info for it
            if self.map.get_terrain(x, y).owner is None:
                text = "Owner: Neutral"
            elif self.map.get_terrain(x, y).owner.ID == PLAYER1:
                text = "Owner: Red"
            elif self.map.get_terrain(x, y).owner.ID == PLAYER2:
                text = "Owner: Blue"
            self.terrain_text.text.append(text)

            text = "HP: " + str(self.map.get_terrain(x, y).hp)
            self.terrain_text.text.append(text)

    def print_atk_preview(self, x, y, x2, y2):
        # attacker_dmg = self.map.get_unit(x, y).damage
        # defense = self.map.get_terrain(x2, y2).defense
        #
        #
        #
        # self.preview_text.text.clear()
        # damage = attacker_dmg - defense
        # if damage < 0:
        #     damage = 0
        self.preview_text.text.clear()
        text = "Damage you will deal PRINT NOT IMPLEMENTED"  # + str(damage)
        self.preview_text.text.append(text)

    def print_merge_preview(self, x, y, x2, y2):
        unit1 = self.map.get_unit(x, y)
        unit2 = self.map.get_unit(x2, y2)
        self.preview_text.text.clear()
        text = "You will merge unit at " + str(x) + ", " + str(y) + " with unit " + str(x2) + ", " + str(y2)
        self.preview_text.text.append(text)

        hp = unit2.hp + unit1.hp
        excess = 0
        if hp > FULL_HP:
            excess = hp - FULL_HP
            # TODO add fund depending on excess hp
            hp = FULL_HP
        text = "Merged unit will have " + str(hp) + "hp with " + str(excess) + " excess"
        self.preview_text.text.append(text)

    def print_factory_preview(self, selected_unit, player):
        if selected_unit is None:
            self.preview_text.text.clear()
            text = "You have " + str(player.funds) + " funds available"
            self.preview_text.text.append(text)
            return None, '.'
        else:
            unit = factory_units[selected_unit]
            name_symbol = unit_name_symbol[unit]
            name = name_symbol[0]
            symbol = name_symbol[1]
            cost = unit_costs[unit]
            self.preview_text.text.clear()
            text = name + ": " + str(cost)
            self.preview_text.text.append(text)
            return unit, symbol

    # def interpret_ai(self):
    #     player = self.players[self.turn]
    #     other_player = self.players[(self.turn + 1) % NB_PLAYER]
    #     unit = player.units[0]
    #     enn = other_player.units[0]
    #     action = self.skynet.get_action()
    #     mvt = action[0]
    #     attack = action[1]
    #     illegal_move = True
    #     self.highlight(unit.mvt_type, unit.movement, unit.fuel, unit.x, unit.y)
    #     if self.map.is_highlight(unit.x + mvt[0], unit.y + mvt[1]):
    #         self.map.move_unit(unit.x, unit.y, unit.x + mvt[0], unit.y + mvt[1])
    #         if not (attack[0] == 0 and attack[1] == 0):
    #             self.direct_atk_enemy_highlight(unit.x, unit.y)
    #             if self.map.is_atk_highlight(unit.x + attack[0], unit.y + attack[1]):
    #                 unitx = unit.x
    #                 unity = unit.y
    #                 ennx = enn.x
    #                 enny = enn.y
    #                 self.atk_target(unit.x, unit.y, unit.x + attack[0], unit.y + attack[1])
    #                 illegal_move = False
    #                 if not player.units:
    #                     self.erase_highlights()
    #                     self.skynet.get_reward(-1, unitx, unity, 0, ennx, enny, enn.get_binary_hp(),
    #                                            self.scenario_players[0])
    #                     print("Skynet attacked and was destroyed")
    #                     print("Reset on scenario turn " + str(self.scenario_counter))
    #                     self.reset()
    #                     return
    #                 elif not other_player.units:
    #                     self.erase_highlights()
    #                     self.skynet.get_reward(1, unitx, unity, unit.get_binary_hp(), ennx, enny, 0,
    #                                            self.scenario_players[0])
    #                     print("Skynet attacked and destroyed the enemy")
    #                     print("Ended on scenario turn " + str(self.scenario_counter))
    #                     self.reset()
    #                     return
    #             else:
    #                 self.map.move_unit(unit.x, unit.y, unit.x - mvt[0], unit.y - mvt[1])
    #         else:
    #             illegal_move = False
    #     self.erase_highlights()
    #     self.new_turn()
    #     self.draw()
    #     self.scenario_counter += 1
    #
    #     # STATIC AI PHASE
    #     new_enn_x, new_enn_y, atk_x, atk_y = static_ai.get_action(enn.x, enn.y, unit.x, unit.y)
    #     self.map.move_unit(enn.x, enn.y, new_enn_x, new_enn_y)
    #     enn_x = new_enn_x
    #     enn_y = new_enn_y
    #     unitx = unit.x
    #     unity = unit.y
    #     result = "Something wrong happened, I'm not suppose to print"
    #     if not (atk_x == atk_y == 0):
    #         self.atk_target(enn_x, enn_y, enn_x + atk_x, enn_y + atk_y)
    #         if not self.player1.units:
    #             result = "AI killed Skynet by attacking it"
    #         elif not self.player2.units:
    #             result = "AI killed himself by attacking Skynet"
    #     self.new_turn()
    #     # REWARD
    #     if not self.player1.units:  # if skynet died
    #         enn = self.player2.units[0]
    #         self.skynet.get_reward(-1, unitx, unity, 0, enn.x, enn.y, enn.get_binary_hp(), self.scenario_players[0])
    #         print(result)
    #         self.reset()
    #         return
    #     elif not self.player2.units:  # if enn died
    #         if illegal_move:
    #             print(f'Illegal move given: {action}')
    #             reward = -1
    #         else:
    #             reward = 1
    #         self.skynet.get_reward(reward, unit.x, unit.y, unit.get_binary_hp(), enn_x, enn_y, 0,
    #                                self.scenario_players[0])
    #         print("Success!")
    #         print(result)
    #         print("At turn: " + str(self.turn_counter))
    #         self.reset()
    #         return
    #     if illegal_move:
    #         print(f'Illegal move given: {action}')
    #         reward = -1
    #     else:
    #         reward = 0
    #     self.skynet.get_reward(reward, unit.x, unit.y, unit.get_binary_hp(), enn.x, enn.y, enn.get_binary_hp(),
    #                            self.scenario_players[0])
    #
    #     if self.scenario_counter == MAX_SCENARIO_TURN:
    #         print("Ended on scenario turn " + str(MAX_SCENARIO_TURN))
    #         self.reset()
    #         return

    # def interpret_ai(self):
    #     skynet_dealt_damage = False
    #     ai_dealt_damage = False
    #     new_reward = None  # Reward for damaging
    #     player = self.players[self.turn]
    #     other_player = self.players[(self.turn + 1) % NB_PLAYER]
    #     unit = player.units[0]
    #     enn = other_player.units[0]
    #     action = self.skynet.get_action()
    #     mvt = action[0]
    #     attack = action[1]
    #     illegal_move = True
    #     self.highlight(unit.mvt_type, unit.movement, unit.fuel, unit.x, unit.y)
    #     if self.map.is_highlight(unit.x + mvt[0], unit.y + mvt[1]):
    #         self.map.move_unit(unit.x, unit.y, unit.x + mvt[0], unit.y + mvt[1])
    #         if not (attack[0] == 0 and attack[1] == 0):
    #             self.direct_atk_enemy_highlight(unit.x, unit.y)
    #             if self.map.is_atk_highlight(unit.x + attack[0], unit.y + attack[1]):
    #                 skynet_dealt_damage = True
    #                 if self.player1.units[0].hp >= self.player2.units[0].hp:  # Skynet had more HP: attacking first was the good move.
    #                     new_reward = 0
    #                 else:  # Skynet had less HP: RUN, YOU FOOL!
    #                     new_reward = -2
    #                 self.atk_target(unit.x, unit.y, unit.x + attack[0], unit.y + attack[1])
    #                 illegal_move = False
    #                 if not player.units:  # Lost from attacking
    #                     self.erase_highlights()
    #                     self.skynet.set_reward(-2, self.scenario_player_1)
    #                     print("Skynet attacked and was destroyed")
    #                     print("Reset on scenario turn " + str(self.scenario_counter))
    #                     self.reset()
    #                     return
    #                 elif not other_player.units:  # Won from attacking
    #                     self.erase_highlights()
    #                     self.skynet.set_reward(0, self.scenario_player_1)
    #                     print("Skynet attacked and destroyed the enemy")
    #                     print("Ended on scenario turn " + str(self.scenario_counter))
    #                     self.reset()
    #                     return
    #             else:
    #                 self.map.move_unit(unit.x, unit.y, unit.x - mvt[0], unit.y - mvt[1])
    #         else:
    #             illegal_move = False
    #     self.erase_highlights()
    #     self.new_turn()
    #     self.draw()
    #     self.scenario_counter += 1
    #
    #     # STATIC AI PHASE
    #     new_enn_x, new_enn_y, atk_x, atk_y = static_ai.get_action(enn.x, enn.y, enn.hp, unit.x, unit.y, unit.hp)
    #     self.map.move_unit(enn.x, enn.y, new_enn_x, new_enn_y)
    #     enn_x = new_enn_x
    #     enn_y = new_enn_y
    #     result = "Something wrong happened, I'm not suppose to print"
    #     if not (atk_x == atk_y == 0):
    #         self.atk_target(enn_x, enn_y, enn_x + atk_x, enn_y + atk_y)
    #         if not self.player1.units:  # Lost by being attacked
    #             result = "AI killed Skynet by attacking it"
    #         elif not self.player2.units:  # Won by being attacked
    #             result = "AI killed himself by attacking Skynet"
    #     self.new_turn()
    #     # REWARD
    #     if not self.player1.units:  # Skynet lost by being attacked
    #         self.skynet.set_reward(-2, self.scenario_player_1)
    #         print(result)
    #         self.reset()
    #         return
    #     elif not self.player2.units:  # Skynet won by counter attacking
    #         if illegal_move:
    #             print(f'Illegal move given: {action} --- {self.skynet.skynet_pos_x, self.skynet.skynet_pos_y}')
    #             exit()
    #             reward = -2
    #         else:
    #             reward = -1
    #             if skynet_dealt_damage:  # If Skynet attacked prior to that and the enemy dies, then we want the true reward.
    #                 reward = new_reward
    #         self.skynet.get_reward(reward, unit.x, unit.y, 1, enn_x, enn_y, self.scenario_players[0])  # Must have more HP
    #         print("Success!")
    #         print(result)
    #         print("At turn: " + str(self.turn_counter))
    #         self.reset()
    #         return
    #     if illegal_move:  # No one died, but illegal move
    #         print(f'Illegal move given: {action} --- {self.skynet.skynet_pos_x, self.skynet.skynet_pos_y}')
    #         exit()
    #         reward = -2
    #     else:
    #         reward = -1
    #         if skynet_dealt_damage:  # Skynet dealt damage, so we take the new reward instead.
    #             reward = new_reward
    #     if self.player1.units[0].hp == self.player2.units[0].hp:
    #         rel_hp = 2
    #     elif self.player1.units[0].hp > self.player2.units[0].hp:
    #         rel_hp = 1
    #     else:
    #         rel_hp = 0
    #     self.skynet.get_reward(reward, unit.x, unit.y, rel_hp, enn.x, enn.y, self.scenario_players[0])
    #
    #     if self.scenario_counter == MAX_SCENARIO_TURN:
    #         print("Ended on scenario turn " + str(MAX_SCENARIO_TURN))
    #         self.reset()
    #         return

    def interpret_ai(self):
        new_reward = None
        player = self.players[self.turn]
        other_player = self.players[(self.turn + 1) % NB_PLAYER]
        unit = player.units[0]
        enn = other_player.units[0]
        self.skynet.set_param(unit.x, unit.y, enn.x, enn.y)
        action = self.skynet.get_action()
        mvt = action[0]
        attack = action[1]
        illegal_move = True
        self.highlight(unit.mvt_type, unit.movement, unit.fuel, unit.x, unit.y)
        if self.map.is_highlight(unit.x + mvt[0], unit.y + mvt[1]):
            self.map.move_unit(unit.x, unit.y, unit.x + mvt[0], unit.y + mvt[1])
            if not (attack[0] == 0 and attack[1] == 0):
                self.direct_atk_enemy_highlight(unit.x, unit.y)
                if self.map.is_atk_highlight(unit.x + attack[0], unit.y + attack[1]):
                    unit_x, unit_y, enx, eny = unit.x, unit.y, enn.x, enn.y
                    self.atk_target(unit.x, unit.y, unit.x + attack[0], unit.y + attack[1])
                    illegal_move = False
                    if not player.units:  # Lost from attacking
                        if SCENARIO == RUNAWAY:
                            self.erase_highlights()
                            self.skynet.set_reward(-2, self.scenario_player_1)
                            print("Skynet attacked and was destroyed")
                            print("Reset on scenario turn " + str(self.scenario_counter))
                            self.reset()
                        elif SCENARIO == ATTACK:  # This shouldn't happen
                            self.erase_highlights()
                            print("Skynet attacked the AI in the Attack scenario and died. This is not normal")
                            self.reset()
                        else:
                            self.erase_highlights()
                            self.skynet.set_reward(0, self.scenario_player_1)
                            print("Skynet attacked and was destroyed")
                            print("Reset on scenario turn " + str(self.scenario_counter))
                            self.reset()
                        return
                    elif not other_player.units:  # Won from attacking
                        if SCENARIO == RUNAWAY:  # This shouldn't happen
                            self.erase_highlights()
                            print("Skynet attacked the AI in the Runaway scenario and won. This is not normal")
                            self.reset()
                        elif SCENARIO == ATTACK:
                            self.erase_highlights()
                            self.skynet.set_reward(0, self.scenario_player_1)
                            print("Skynet attacked and destroyed the AI")
                            print("Reset on scenario turn " + str(self.scenario_counter))
                            self.reset()
                        else:
                            self.erase_highlights()
                            self.skynet.set_reward(0, self.scenario_player_1)
                            print("Skynet attacked and destroyed the AI")
                            print("Reset on scenario turn " + str(self.scenario_counter))
                            self.reset()
                        return
                else:
                    self.map.move_unit(unit.x, unit.y, unit.x - mvt[0], unit.y - mvt[1])
            else:
                illegal_move = False
                if SCENARIO == ATTACK or SCENARIO == STALEMATE:
                    self.direct_atk_enemy_highlight(unit.x, unit.y)
                    if self.map.is_atk_highlight(enn.x, enn.y):  # The enemy was in range and Skynet didn't attack
                        new_reward = -2

        self.erase_highlights()
        self.new_turn()
        self.draw()
        self.scenario_counter += 1

        # STATIC AI PHASE
        if SCENARIO == RUNAWAY or SCENARIO == STALEMATE:
            new_enn_x, new_enn_y, atk_x, atk_y = agr_ai.get_action(enn.x, enn.y, enn.hp, unit.x, unit.y, unit.hp)
        else:
            new_enn_x, new_enn_y, atk_x, atk_y = run_ai.get_action(enn.x, enn.y, enn.hp, unit.x, unit.y, unit.hp)
        self.map.move_unit(enn.x, enn.y, new_enn_x, new_enn_y)
        enx = new_enn_x
        eny = new_enn_y
        unit_x = unit.x
        unit_y = unit.y
        result = "Something wrong happened, I'm not suppose to print"
        if not (atk_x == atk_y == 0):
            if unit.hp == 100:
                new_reward = -2
            self.atk_target(enx, eny, enx + atk_x, eny + atk_y)
            if not self.player1.units:  # Lost by being attacked
                result = "AI killed Skynet by attacking it"
            elif not self.player2.units:  # Won by being attacked
                result = "AI killed himself by attacking Skynet"
        self.new_turn()

        # REWARD
        if not self.player1.units:  # Skynet lost by being attacked
            if SCENARIO == RUNAWAY:
                self.skynet.set_reward(-2, self.scenario_player_1)
                print(result)
                self.reset()
            elif SCENARIO == ATTACK:  # This shouldn't happen
                print(result)
                print("The AI attacked Skynet in the scenario attack and won, this is not suppose to happen")
                self.reset()
            else:
                self.skynet.set_reward(-2, self.scenario_player_1)
                print(result)
                self.reset()
            return
        elif not self.player2.units:  # Skynet won by counter attacking
            if illegal_move:
                print(f'Illegal move given: {action} --- {self.skynet.skynet_pos_x, self.skynet.skynet_pos_y}')
                exit()
            else:
                if SCENARIO == RUNAWAY:  # This shouldn't happen
                    print(result)
                    print("The AI attacked Skynet in the scenario runaway and lost, this is not suppose to happen")
                    self.reset()
                elif SCENARIO == ATTACK:
                    self.skynet.set_reward(0, self.scenario_player_1)
                    print(result)
                    print("The AI attacked Skynet in the scenario attack and lost,"
                          "the training AI is not suppose to behave this way"
                          "this is not behavior we want to teach Skynet")
                    self.reset()
                else:
                    self.skynet.get_reward(0, unit_x, unit_y, enx, eny, self.scenario_player_1)
                    print(result)
                    print("The AI attacked Skynet in the scenario stalemate and lost,"
                          "The training AI is not suppose to behave this way."
                          "I'm not sure this is behavior we want to teach Skynet")
                    self.reset()
            return
        if illegal_move:  # No one died, but illegal move
            print(f'Illegal move given: {action} --- {self.skynet.skynet_pos_x, self.skynet.skynet_pos_y}')
            exit()
        else:
            if SCENARIO == RUNAWAY:  # Skynet survived, positive reward
                reward = 0
            elif SCENARIO == ATTACK:  # Skynet didn't kill the enemy yet, neutral reward
                reward = -1
            else:
                reward = -1 # Skynet didn't kill the enemy yet, neutral reward

        if new_reward:  # If he didn't attack and could in stalemate or attack scenario or got attacked first in stalemate
            self.skynet.set_reward(new_reward, self.scenario_player_1)
        else:
            self.skynet.get_reward(reward, unit.x, unit.y, enn.x, enn.y, self.scenario_player_1)

        if self.scenario_counter == MAX_SCENARIO_TURN:
            print("Ended on scenario turn " + str(MAX_SCENARIO_TURN))
            self.reset()
            return

    def ask_interpret_skynet_vs_skynet(self):
        player = self.players[self.turn]
        other_player = self.players[(self.turn+1) % NB_PLAYER]
        skynet = self.skynets[self.turn]
        other_skynet = self.skynets[(self.turn+1) % NB_PLAYER]
        unit = player.units[0]
        enn = self.players[(self.turn+1) % NB_PLAYER].units[0]
        skynet.set_param(unit.x, unit.y, enn.x, enn.y)
        action = skynet.get_action()
        mvt = action[0]
        attack = action[1]
        illegal_move = True
        self.highlight(unit.mvt_type, unit.movement, unit.fuel, unit.x, unit.y)
        if self.map.is_highlight(unit.x + mvt[0], unit.y + mvt[1]):
            self.map.move_unit(unit.x, unit.y, unit.x + mvt[0], unit.y + mvt[1])
            if not (attack[0] == 0 and attack[1] == 0):
                self.direct_atk_enemy_highlight(unit.x, unit.y)
                if self.map.is_atk_highlight(unit.x + attack[0], unit.y + attack[1]):
                    unitx = unit.x
                    unity = unit.y
                    ennx = enn.x
                    enny = enn.y
                    self.atk_target(unit.x, unit.y, unit.x + attack[0], unit.y + attack[1])
                    illegal_move = False
                    if not player.units:  # Current Skynet loses
                        self.erase_highlights()
                        skynet.set_reward(-2, self.scenario_players[self.turn])
                        other_skynet.get_reward(0, ennx, enny, unitx, unity, self.scenario_players[(self.turn+1) % NB_PLAYER])
                        print("Skynet" + str(self.turn+1) + " attacked and was destroyed")
                        print("Reset on scenario turn " + str(self.scenario_counter))
                        self.reset()
                        return
                    elif not other_player.units:  # Current Skynet wins
                        self.erase_highlights()
                        skynet.set_reward(0, self.scenario_players[self.turn])
                        other_skynet.set_reward(-2, self.scenario_players[(self.turn+1) % NB_PLAYER])
                        print("Skynet" + str(self.turn+1) + " attacked and destroyed the enemy")
                        print("Ended on scenario turn " + str(self.scenario_counter))
                        self.reset()
                        return
                else:
                    self.map.move_unit(unit.x, unit.y, unit.x - mvt[0], unit.y - mvt[1])
            else:
                illegal_move = False
        self.erase_highlights()
        self.new_turn()
        self.draw()
        self.scenario_counter += 1
        if self.next_reward is not None:  # No one won nor lost
            other_skynet.get_reward(self.next_reward, enn.x, enn.y, unit.x, unit.y, self.scenario_player_1)
        else:
            other_skynet.en_pos_x = unit.x
            other_skynet.en_pos_y = unit.y
        if self.scenario_counter == MAX_SCENARIO_TURN:
            print("Ended on scenario turn " + str(MAX_SCENARIO_TURN))
            self.reset()
            return
        if illegal_move:
            print(f'Illegal move given: {action}')
            self.next_reward = -1
        else:
            self.next_reward = 0

    def ask_interpret_skynet(self):
        player = self.players[self.turn]
        enn = self.players[(self.turn+1)% NB_PLAYER].units[0]
        unit = player.units[0]
        self.skynet.set_param(unit.x, unit.y, enn.x, enn.y)
        action = self.skynet.get_action()
        mvt = action[0]
        attack = action[1]
        self.highlight(unit.mvt_type, unit.movement, unit.fuel, unit.x, unit.y)
        if self.map.is_highlight(unit.x + mvt[0], unit.y + mvt[1]):
            self.map.move_unit(unit.x, unit.y, unit.x + mvt[0], unit.y + mvt[1])
            if not (attack[0] == 0 and attack[1] == 0):
                self.direct_atk_enemy_highlight(unit.x, unit.y)
                if self.map.is_atk_highlight(unit.x + attack[0], unit.y + attack[1]):
                    self.atk_target(unit.x, unit.y, unit.x + attack[0], unit.y + attack[1])
                else:
                    print(f'Illegal move given: {action}')
                    self.map.move_unit(unit.x, unit.y, unit.x - mvt[0], unit.y - mvt[1])
        else:
            print(f'Illegal move given: {action}')
        self.erase_highlights()
        if self.player1.units and self.player2.units:
            self.skynet.set_param(unit.x, unit.y, enn.x, enn.y)

    def get_random_pos(self, nx=None, ny=None):
        wrong = [(3, 2), (2, 3), (3, 3), (4, 3), (3, 4)]
        if nx and ny is None:
            x = random.randint(0, GRID_X_SIZE - 1)
            y = random.randint(0, GRID_X_SIZE - 1)
            while (x, y) in wrong:
                x = random.randint(0, GRID_X_SIZE - 1)
                y = random.randint(0, GRID_X_SIZE - 1)
            return x, y
        else:
            x = random.randint(0, GRID_X_SIZE - 1)
            y = random.randint(0, GRID_X_SIZE - 1)
            while (x == nx and y == ny) or (x, y) in wrong:
                x = random.randint(0, GRID_X_SIZE - 1)
                y = random.randint(0, GRID_X_SIZE - 1)
            return x, y

    def get_random_scenario(self):
        x = random.randint(0, 2)
        y, lhp, rhp = None, None, None
        if x == 0:  # Both high: Stalemate
            y = 0
            lhp = 1
            rhp = 1
        elif x == 1:  # Run away
            y = 2
            lhp = 0
            rhp = 1
        elif x == 2:  # Attack
            y = 1
            lhp = 1
            rhp = 0
        return x, y, lhp, rhp

    def iterative_attack_training(self):
        self.skynet.epsilon = 0
        for a in range(0, 7):
            for b in range(0, 7):
                enx, eny = a, b
                for y in range(0, 7):
                    for x in range(0, 7):
                        if not (x == enx and y == eny) and (abs(enx - x) + abs(eny - y)) <= 4:
                            self.skynet.set_param(x, y, enx, eny)
                            learning = True
                            while learning:
                                self.skynet.epsilon = 1
                                print(x, y, enx, eny)
                                action = self.skynet.get_action()
                                mvt = action[0]
                                attack = action[1]
                                # print("Got these action from skynet")
                                # print(mvt, attack)
                                if (x + mvt[0] + attack[0]) == enx and (y + mvt[1] + attack[1]) == eny: #1 == (abs(enx - x + mvt[0]) + abs(eny - y + mvt[1])) and

                                    print("that was right")

                                    self.skynet.set_reward(0, 2)
                                    learning = False
                                else:
                                    # print("that was wrong")
                                    # print(str(abs(enx - x + mvt[0]) + abs(eny - y + mvt[1])) + " Needed to be 1, "
                                    #       + str(x + mvt[0] + attack[0]) + " Needed to be " + str(enx) + ", " +
                                    #       str(y + mvt[1] + attack[1]) + " Needed to be " + str(eny))
                                    self.skynet.set_reward(-2, 2)
                                    self.skynet.set_param(x, y, enx, eny)
        self.skynet.epsilon = 1
        self.iterative_training = False
        f = open('skynet_q_table_attack.pickle', 'wb')
        f.write(pickle.dumps(self.skynet.q_table))
        f.close()
        exit()







"""
    Player class holds info for a player, His ID, units, buildings, CO and funds
"""


class Player:
    def __init__(self, player_id, co):
        self.ID = player_id
        self.units = []
        self.buildings = []
        self.CO = co
        self.funds = STARTING_FUNDS


"""
Button class that is used to simulate a button, pretty much such a square with text on it and a isOver function
that indicates if the mouse is over the button
Need to be refined possibly
"""


class Button:
    def __init__(self, screen, color, x, y, width, height, text=''):
        self.screen = screen
        self.color = LIGHTGREY
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, outline=True):
        # draws button and text on screen
        if outline:
            pg.draw.rect(self.screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pg.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pg.font.SysFont('timesnewroman', 40)
            text = font.render(self.text, 1, BLACK)
            self.screen.blit(text, (
                math.floor(self.x + (self.width / 2 - text.get_width() / 2)),
                math.floor(self.y + (self.height / 2 - text.get_height() / 2))))

    def isOver(self, x, y):  # indicates is mouse is over button
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                return True
        return False


"""
Textbox class that is used to simulate a textbox
Still in prototype phase I would say
"""


class Textbox:
    def __init__(self, screen, x, y, width, height):
        self.screen = screen
        self.x = x
        self.y = y
        self.font_size = 16
        self.font = pg.font.SysFont("Times New Roman", self.font_size)
        self.width = width
        self.height = height
        self.image = pg.Surface((width, height))
        self.text = [""]
        self.border = 2

    def clear(self):  # clear the screen of text
        self.image.fill(BLACK)
        # this is the background of the text box, we draw a smaller box over to make it look like it has a border
        pg.draw.rect(self.image, WHITE,
                     (self.border, self.border, self.width - self.border * 2, self.height - self.border * 2))
        self.screen.blit(self.image, (self.x, self.y))

    def draw(self):
        # to draw text, the function goes through a list of strings and prints them on the text box,
        # it adds the font_size to y every string to simulate a new line
        self.clear()
        line = 0
        for text in self.text:
            text = self.font.render(text, 1, BLACK)
            self.screen.blit(text, (self.x + self.border, self.y + line * self.font_size))
            line += 1


# create the game object
g = Game()
g.new()
while True:
    g.run()