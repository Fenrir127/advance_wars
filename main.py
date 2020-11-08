import pygame as pg
import sys
from map import *
from os import path
import math


class Game:
    """Game has references to the Map and a list of all the sprites.
    Game takes care of all user interactions and calls map most of the time for information inquiries
    and changing the gameworld such as moving a unit."""

    def __init__(self):
        pg.init()

        # General game settings and initialization
        self.screen = pg.display.set_mode((SCREEN_WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()

        self.load_data()  # used for future loading purposes

    def load_data(self):  # used for future loading purposes, does nothing for now
        pass

    def new(self):
        # initialize all variables and do all the setup for a new game
        # This is where we initialize the buttons and the text boxes
        self.textboxes = []
        self.unit_text = Textbox(self.screen, 1024, 0, 240, 256)
        self.textboxes.append(self.unit_text)
        self.terrain_text = Textbox(self.screen, 1264, 0, 240, 256)
        self.textboxes.append(self.terrain_text)
        self.preview_text = Textbox(self.screen, 1024, 256, 480, 256)
        self.textboxes.append(self.preview_text)

        # This is where we create the buttons
        self.buttons_list = []
        self.cancel_btn = Button(self.screen, WHITE, 1264, 640, 240, 128, "Cancel")
        self.end_turn_btn = Button(self.screen, WHITE, 1024, 640, 240, 128, "End Turn")
        self.special_btn = Button(self.screen, WHITE, 1264, 512, 240, 128, "Cptr/Rfl/Mrg")
        self.attack_btn = Button(self.screen, WHITE, 1024, 512, 240, 128, "Attack")
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

        # Terrain
        self.plain_image = pg.image.load(path.join(img_folder, 'plain.png')).convert_alpha()
        self.river_image = pg.image.load(path.join(img_folder, 'river.png')).convert_alpha()
        self.wood_image = pg.image.load(path.join(img_folder, 'wood.png')).convert_alpha()
        self.mountain_image = pg.image.load(path.join(img_folder, 'mountain.png')).convert_alpha()
        self.road_image = pg.image.load(path.join(img_folder, 'road.png')).convert_alpha()

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

        # Initialize the players, first number is the player id, second is the CO
        self.player1 = Player(PLAYER1, NEUTRAL)
        self.player2 = Player(PLAYER2, NEUTRAL)
        self.turn = PLAYER1  # turn start player2 but game setup calls end_turn() which ticks turn to player 1
        self.players = [self.player1, self.player2]

        # creates the map and the reference
        self.map = Map(self)

    def run(self):
        # game loop, set self.playing = False to end the game
        self.playing = True

        # Hard coded, player 1 always start the game
        for unit in self.player1.units:
            unit.new_turn()

        while self.playing:  # game loop
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            # self.erase_highlights()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def erase_highlights(self):  # this is currently only used to remove the highlight, usually we'd move pieces around here
        # but we do that in Map when we need to because our game is not in real-time
        # update portion of the game loop
        # self.unit_sprites.update()
        self.foreground_sprites.update()

    def draw_grid(self):  # draws line in a grid
        # stops at 32 width to leave space for text and buttons
        for x in range(0, GRID_WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (GRID_WIDTH, y))

    def draw(self):  # draw everything from bottom to top layer
        # we might have to split the draw functions between the text files and the game map later on
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

    def events(self):
        # catch all events here
        self.end_turn_btn.text = "End turn"
        self.cancel_btn.text = ""
        self.attack_btn.text = ""
        self.special_btn.text = ""
        for event in pg.event.get():
            if event.type == pg.QUIT:  # allow close game
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
            if event.type == pg.MOUSEBUTTONDOWN:  # enters when the user click on something
                x, y = self.get_grid_coord()  # gets the grid coord of where the user clicked in grid x and y
                if x > 31:
                    # if x > 31, that means the user didn't click the map but clicked the button or text box instead
                    # we need to get the position again but this time in pixel.
                    x, y = pg.mouse.get_pos()
                    for button in self.buttons_list:  # checks if any button created are being hovered before clicking
                        if button.isOver(x, y):
                            if button == self.end_turn_btn:
                                self.new_turn()
                else:
                    # if self.map.is_unit(x, y):    # enters if there is a unit where the user clicked
                    self.tile_selected(x, y)  # Function takes care of actions when selecting unit

    def get_grid_coord(self):  # returns the position of the mouse in grid x and y rather than in pixels
        x, y = pg.mouse.get_pos()
        x = math.floor(x / TILESIZE)  # Divide by tile size and floor it to get the tile coord,
        y = math.floor(y / TILESIZE)  # almost everything works in map coordinate except the buttons
        return x, y

    def print_details(self, x, y):
        if self.map.is_unit(x, y):
            self.print_unit_details(x, y)
        else:
            self.unit_text.text.clear()
        self.print_terrain_details(x, y)

    def tile_selected(self, x, y):  # Function takes care of actions when selecting unit, for now, only movement
        # Display options after selecting unit
        # Assume user want to move unit for now
        # x, y are the current position while x2, y2 are the new position.
        self.erase_highlights()
        self.print_details(x, y)
        if self.map.is_unit(x, y):
            unit = self.map.get_unit(x, y)
            if unit.player.ID == self.turn:
                if unit.available:
                    moved, x2, y2 = self.move_unit(x, y)
                    if moved:  # if the unit moved, it can proceed to attack another unit in range
                        self.options(x, y, x2, y2)  # This function takes care of all attacking shenanigans
                    if not unit.available:
                        unit.end_turn()
                    self.erase_highlights()
            else:
                self.highlight_enemy(self.map.get_unit_mvt_type(x, y), self.map.get_mvt(x, y), x, y)

    def move_unit(self, x, y):
        # This function takes care of everything related to moving a unit.
        # it takes the x and y of the unit selected, highlight the available movement
        # draws the highlight and moves the unit if needed.
        self.highlight(self.map.get_unit_mvt_type(x, y), self.map.get_mvt(x, y), x, y)  # Highlights the valid tiles
        self.end_turn_btn.text = "End Mvt"
        self.cancel_btn.text = "Cancel"
        self.draw()  # draws the highlight
        position_selected = False
        moved = False
        while not position_selected:  # loops until the user clicks a tile
            event = pg.event.wait()
            if event.type == pg.MOUSEBUTTONDOWN:  # enters when the user clicks on tile
                x2, y2 = self.get_grid_coord()  # Coordinate of the new tile clicked
                if x2 > 31:  # if x > 31, the user clicked the buttons of a textbox
                    x2, y2 = pg.mouse.get_pos()  # gets the position again but this time in pixel.
                    if self.cancel_btn.isOver(x2, y2):  # Cancel the move order, currently doesn't really od anything but might change later on
                        position_selected = True
                    elif self.end_turn_btn.isOver(x2, y2):
                        moved = False
                        position_selected = True
                        self.map.get_unit(x, y).end_turn()
                elif self.map.is_highlight(x2, y2) and not self.map.is_unit(x2, y2):
                    # if the tile has a highlight and no unit on it, it is valid and the unit moves
                    self.map.move_unit(x, y, x2, y2)  # moves the unit, Map takes care of it
                    self.draw()
                    moved = True
                    position_selected = True
                    self.print_details(x2, y2)
                elif self.map.is_unit(x2, y2) and self.map.is_highlight(x2, y2):  # Merge 2 units
                    if x == x2 and y == y2:
                        moved = True
                        position_selected = True
                    else:
                        self.merge_unit(x, y, x2, y2)
                        self.print_details(x2, y2)
        self.erase_highlights()
        return moved, x2, y2

    def highlight(self, mvt_type, mvt, x, y, direction="None"):
        # This function takes care of highlighting tiles of available movement for a unit
        # It is a recurring function that stops once an impassable terrain is reached or the max movement is reached
        # It takes the unit mvt type (there are 7 in the game), the unit mvt (how much it can move) and x and y

        # TODO Feel free to optimise this function!


        if mvt == -1 or x < 0 or x > 31 or y < 0 or y > 23:  # if out of movement or out of the game grid, stop
            return

        if not self.map.get_tile_mvt_cost(mvt_type, x, y):
            return
            # enters if the terrain is impassable for the given unit and stop. We know it is impassable because the
            # mvt cost for a given type will be 0 if the unit can't go there.
            # (ex tank in water, tank mvt_type is TREAD, river tread_mvt_cost = 0)

        if self.map.is_unit(x, y):
            if self.map.get_unit(x, y).player.ID != self.turn:
                return

        self.map.highlight_tile(x, y)

        # This is where the function loops on itself, it goes in all 4 directions to check for potential valid tiles
        # to save some iterations, it doesn't go back the way it just came. AKA if it's going upwards, it won't go back
        # down immediately but, it might can go up, left, down and right and check the same tile again.
        # This can be improved

        if direction != "down":
            if y - 1 >= 0:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x, y - 1)
                if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight(mvt_type, mvt - mvt_cost, x, y - 1, "up")  # going up
        if direction != "right":
            if x - 1 >= 0:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x - 1, y)
                if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight(mvt_type, mvt - mvt_cost, x - 1, y, "left")  # going left
        if direction != "left":
            if x + 1 <= 31:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x + 1, y)
                if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight(mvt_type, mvt - mvt_cost, x + 1, y, "right")  # going right
        if direction != "up":
            if y + 1 <= 23:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x, y + 1)
                if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight(mvt_type, mvt - mvt_cost, x, y + 1, "down")  # going down

    def highlight_enemy(self, mvt_type, mvt, x, y, direction="None"):
        # This function takes care of highlighting tiles of available movement for a unit
        # It is a recurring function that stops once an impassable terrain is reached or the max movement is reached
        # It takes the unit mvt type (there are 7 in the game), the unit mvt (how much it can move) and x and y

        # TODO Feel free to optimise this function!

        if x < 0 or x > 31 or y < 0 or y > 23:  # if out of movement or out of the game grid, stop
            return

        if not self.map.get_tile_mvt_cost(mvt_type, x, y):
            self.map.atk_highlight_tile(x, y)
            return
            # enters if the terrain is impassable for the given unit and stop. We know it is impassable because the
            # mvt cost for a given type will be 0 if the unit can't go there.
            # (ex tank in water, tank mvt_type is TREAD, river tread_mvt_cost = 0)

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
                if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight_enemy(mvt_type, mvt - mvt_cost, x, y - 1, "up")  # going up
                else:
                    self.direct_atk_highlight(x, y)
        if direction != "right":
            if x - 1 >= 0:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x - 1, y)
                if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight_enemy(mvt_type, mvt - mvt_cost, x - 1, y, "left")  # going left
                else:
                    self.direct_atk_highlight(x, y)
        if direction != "left":
            if x + 1 <= 31:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x + 1, y)
                if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight_enemy(mvt_type, mvt - mvt_cost, x + 1, y, "right")  # going right
                else:
                    self.direct_atk_highlight(x, y)
        if direction != "up":
            if y + 1 <= 23:
                mvt_cost = self.map.get_tile_mvt_cost(mvt_type, x, y + 1)
                if mvt - mvt_cost > -1:  # enters if the unit has enough mvt left to move onto this tile
                    self.highlight_enemy(mvt_type, mvt - mvt_cost, x, y + 1, "down")  # going down
                else:
                    self.direct_atk_highlight(x, y)

    def options(self, old_x, old_y, x, y):
        # This function takes care of handling everything related to attacking.
        # It highlights the tiles that can be attacked and attack the corresponding
        # It essentially has the same structure as move_unit() with some different function in the ifs and whiles
        # it can be cancelled by clicking the cancel button, as of the call of this function, the unit has moved to a different location from it's original.
        # If we want to cancel everything, we need to move it back to it's original spot and we need the old x and y for that
        self.direct_atk_enemy_highlight(x, y)  # Highlights tiles that can be attacked
        self.draw()

        target_confirmed = False
        target_selected = False
        attacked = False
        while not target_confirmed:  # loops until the user clicks a tile
            event = pg.event.wait()
            if event.type == pg.MOUSEBUTTONDOWN:  # enters when the user clicks on tile
                x2, y2 = self.get_grid_coord()
                if x2 > 31:
                    x2, y2 = pg.mouse.get_pos()
                    if self.cancel_btn.isOver(x2, y2):
                        target_confirmed = True
                        self.map.move_unit(x, y, old_x, old_y)  # Moves unit back if the user cancels
                    elif self.end_turn_btn.isOver(x2, y2):
                        target_confirmed = True
                    elif self.attack_btn.isOver(x2, y2) and target_selected:
                        self.atk_target(x, y, target_selected[0], target_selected[1])
                        target_confirmed = True
                        self.draw()
                    elif self.special_btn.isOver(x2, y2) and target_selected:
                        self.capture_building(x, y)
                        target_confirmed = True
                elif self.map.is_atk_highlight(x2, y2):
                    self.print_details(x2, y2)
                    self.print_atk_preview(x, y, x2, y2)
                    self.attack_btn.text = "Confirm Atk"
                    target_selected = (x2, y2)
                    self.draw()
                    # attacked = self.atk_target(x, y, x2, y2)
                    # if attacked:
                    #     target_confirmed = True
                elif self.map.get_terrain(x2, y2).type == BUILDING and x2 == x and y2 == y:
                    if self.map.get_terrain(x2, y2).owner != self.turn:
                        self.special_btn.text = "Capture"
                        target_selected = True
                        self.draw()
                        target_selected = True
                else:
                    self.print_details(x2, y2)
                    self.draw()
                # target_confirmed = True  # otherwise nothing and it removes the highlights in the update
        return attacked

    def direct_atk_highlight(self, x, y):
        # highlight tile that can be attacked
        # only direct attacks are implemented, so all unit can attack other unit directly adjacent to themn
        if y - 1 >= 0:
            self.map.atk_highlight_tile(x, y - 1)  # up
        if x - 1 >= 0:
            self.map.atk_highlight_tile(x - 1, y)  # left
        if x + 1 <= 31:
            self.map.atk_highlight_tile(x + 1, y)  # right
        if y + 1 <= 23:
            self.map.atk_highlight_tile(x, y + 1)  # down

    def direct_atk_enemy_highlight(self, x, y):
        # highlight tile that can be attacked
        # only direct attacks are implemented, so all unit can attack other unit directly adjacent to themn
        if y - 1 >= 0:
            if self.map.is_unit(x, y - 1):
                if self.map.get_unit(x, y - 1).player.ID != self.turn:
                    self.map.atk_highlight_tile(x, y - 1)  # up
        if x - 1 >= 0:
            if self.map.is_unit(x - 1, y):
                if self.map.get_unit(x - 1, y).player.ID != self.turn:
                    self.map.atk_highlight_tile(x - 1, y)  # left
        if x + 1 <= 31:
            if self.map.is_unit(x + 1, y):
                if self.map.get_unit(x + 1, y).player.ID != self.turn:
                    self.map.atk_highlight_tile(x + 1, y)  # right
        if y + 1 <= 23:
            if self.map.is_unit(x, y + 1):
                if self.map.get_unit(x, y + 1).player.ID != self.turn:
                    self.map.atk_highlight_tile(x, y + 1)  # down

    def capture_building(self, x, y):
        unit = self.map.get_unit(x, y)
        terrain = self.map.get_terrain(x, y)

        damage = unit.hp
        terrain.hp -= damage
        if terrain.hp < 1:
            terrain.hp = 10
            terrain.owner = unit.player

    def atk_target(self, x, y, x2, y2):
        # this function takes care of damage calculation and updating the corresponding hp
        # Real damage calculation not implemented
        attacker = self.map.get_unit(x, y)
        defender = self.map.get_unit(x2, y2)
        defender_defense = self.map.get_defense(x2, y2)  # TODO maybe put the defense a unit has in the unit class?
        damage_dealt = attacker.damage - defender_defense
        if damage_dealt < 0:
            damage_dealt = 0
        self.preview_text.text.clear()
        text = "You dealt " + str(damage_dealt) + " damage"
        self.preview_text.text.append(text)
        defender.hp -= damage_dealt
        if defender.hp < 1:
            self.map.remove_unit(x2, y2)

    def merge_unit(self, x, y, x2, y2):
        unit1 = self.map.get_unit(x, y)
        unit2 = self.map.get_unit(x2, y2)
        if self.turn == unit1.player and unit1.name == unit2.name and unit2.hp != FULL_HP:
            unit1_hp = unit1.hp
            self.map.remove_unit(x, y)
            unit2.hp += unit1_hp
            if unit2.hp > FULL_HP:
                excess = unit2.hp - FULL_HP
                # TODO add fund depending on excess hp
                unit2.hp = FULL_HP

    def new_turn(self):
        for player in self.players:
            if self.turn == player.ID:
                for unit in player.units:
                    unit.end_turn()
            else:
                for unit in player.units:
                    unit.new_turn()
                for city in player.buildings:
                    city.add_funds()

        self.turn = (self.turn + 1) % NB_PLAYER

        print("player1 funds: " + str(self.player1.funds))
        print("player2 funds: " + str(self.player2.funds))

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
        self.unit_text.text.append(text)
        text = "Mvt: " + str(unit.movement)
        self.unit_text.text.append(text)
        text = "HP: " + str(unit.hp)
        self.unit_text.text.append(text)
        if unit.player.ID == PLAYER1:
            text = "Player: Red"
        elif unit.player.ID == PLAYER2:
            text = "Player: Blue"
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

        if self.map.get_terrain(x, y).type:  # If the terrain type is a building, if also prints the info for it
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
        attacker_dmg = self.map.get_unit(x, y).damage
        defense = self.map.get_terrain(x2, y2).defense

        self.preview_text.text.clear()
        damage = attacker_dmg - defense
        if damage < 0:
            damage = 0
        text = "Damage you will deal " + str(damage)
        self.preview_text.text.append(text)


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
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

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
while True:
    g.new()
    g.run()
