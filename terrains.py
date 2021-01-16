from os import path
from sprites import *
from setting import *

"""
This contains all the information for the different terrain in the game
Nothing should change in there unless there's a way to change terrain in the game which I don't think there is (except building hp)

When you implement a new terrain in the game you need to:
    Make a new terrain class
    make sure id_terrain() in Tile can identify it from the .txt file (give it a letter ex. m for mountain, make sure it's not already taken!!)
    create a sprite class for it (you can copy paste the template of Plain) i'll implement the image for the unit
"""


#TODO do a clean up, lots of info is now unused or redondant and this can be improved



# This is the master class Terrain which only serves to pass on the function get_mvt_cost()
class Terrain:
    def __init__(self, game):
        self.game = game
        self.terrain_type = None
        self.infantry_mvt_cost = None
        self.mech_mvt_cost = None
        self.tires_mvt_cost = None
        self.tread_mvt_cost = None
        self.air_mvt_cost = None
        self.ship_mvt_cost = None
        self.transport_mvt_cost = None

    # This function returns the mvt_cost for one of the 7 mvt_type on a given terrain
    def get_mvt_cost(self, type):
        if type == INFANTRY:
            return self.infantry_mvt_cost
        elif type == MECH:
            return self.mech_mvt_cost
        elif type == TIRES:
            return self.tires_mvt_cost
        elif type == TREAD:
            return self.tread_mvt_cost
        elif type == AIR:
            return self.air_mvt_cost
        elif type == SHIP:
            return self.ship_mvt_cost
        elif type == TRANSPORT:
            return self.transport_mvt_cost
        else:
            print("get_mvt_cost was given the wrong input:")
            print(type)


class Plain(Terrain):
    def __init__(self, game, x, y):
        super().__init__(game)     # the super init doesn't really do anything for now
        self.sprite = Plain_sprite(game, x, y)
        self.name = "Plain"
        self.defense = 1
        self.type = LAND

        # every terrain class must define the mvt cost for all movement types
        # when a mvt_type cost is 0, it means units with this type of mvt cannot go on the tile
        self.infantry_mvt_cost = 1
        self.mech_mvt_cost = 1
        self.tires_mvt_cost = 2
        self.tread_mvt_cost = 1
        self.air_mvt_cost = 1
        self.ship_mvt_cost = 0
        self.transport_mvt_cost = 0


class River(Terrain):
    def __init__(self, game, x, y):
        super().__init__(game)     # the super init doesn't really do anything for now
        self.sprite = River_sprite(game, x, y)
        self.name = "River"
        self.defense = 0
        self.type = LAND

        # every terrain class must define the mvt cost for all movement types
        # when a mvt_type cost is 0, it means units with this type of mvt cannot go on the tile
        self.infantry_mvt_cost = 2
        self.mech_mvt_cost = 1
        self.tires_mvt_cost = 0
        self.tread_mvt_cost = 0
        self.air_mvt_cost = 1
        self.ship_mvt_cost = 0
        self.transport_mvt_cost = 0


class Wood(Terrain):
    def __init__(self, game, x, y):
        super().__init__(game)     # the super init doesn't really do anything for now
        self.sprite = Wood_sprite(game, x, y)
        self.name = "Wood"
        self.defense = 2
        self.type = LAND

        # every terrain class must define the mvt cost for all movement types
        # when a mvt_type cost is 0, it means units with this type of mvt cannot go on the tile
        self.infantry_mvt_cost = 1
        self.mech_mvt_cost = 1
        self.tires_mvt_cost = 3
        self.tread_mvt_cost = 2
        self.air_mvt_cost = 1
        self.ship_mvt_cost = 0
        self.transport_mvt_cost = 0


class Mountain(Terrain):
    def __init__(self, game, x, y):
        super().__init__(game)      # the super init doesn't really do anything for now
        self.sprite = Mountain_sprite(game, x, y)
        self.name = "Mountain"
        self.defense = 4
        self.type = LAND

        # every terrain class must define the mvt cost for all movement types
        # when a mvt_type cost is 0, it means units with this type of mvt cannot go on the tile
        self.infantry_mvt_cost = 2
        self.mech_mvt_cost = 1
        self.tires_mvt_cost = 0
        self.tread_mvt_cost = 0
        self.air_mvt_cost = 1
        self.ship_mvt_cost = 0
        self.transport_mvt_cost = 0

class Sea(Terrain):
    def __init__(self, game, x, y):
        super().__init__(game)       # the super init doesn't really do anything for now
        self.sprite = Sea_sprite(game, x, y)
        self.name = "Sea"
        self.defense = 0
        self.type = WATER

        # every terrain class must define the mvt cost for all movement types
        # when a mvt_type cost is 0, it means units with this type of mvt cannot go on the tile
        self.infantry_mvt_cost = 0
        self.mech_mvt_cost = 0
        self.tires_mvt_cost = 0
        self.tread_mvt_cost = 0
        self.air_mvt_cost = 1
        self.ship_mvt_cost = 1
        self.transport_mvt_cost = 1


class Beach(Terrain):
    def __init__(self, game, x, y):
        super().__init__(game)       # the super init doesn't really do anything for now
        self.sprite = Beach_sprite(game, x, y)
        self.name = "Sea"
        self.defense = 0
        self.type = WATER

        # every terrain class must define the mvt cost for all movement types
        # when a mvt_type cost is 0, it means units with this type of mvt cannot go on the tile
        self.infantry_mvt_cost = 1
        self.mech_mvt_cost = 1
        self.tires_mvt_cost = 2
        self.tread_mvt_cost = 1
        self.air_mvt_cost = 1
        self.ship_mvt_cost = 0
        self.transport_mvt_cost = 1


class Road(Terrain):
    def __init__(self, game, x, y):
        super().__init__(game)     # the super init doesn't really do anything for now
        self.sprite = Road_sprite(game, x, y)
        self.name = "Road"
        self.defense = 0
        self.type = LAND

        # every terrain class must define the mvt cost for all movement types
        # when a mvt_type cost is 0, it means units with this type of mvt cannot go on the tile
        self.infantry_mvt_cost = 1
        self.mech_mvt_cost = 1
        self.tires_mvt_cost = 1
        self.tread_mvt_cost = 1
        self.air_mvt_cost = 1
        self.ship_mvt_cost = 0
        self.transport_mvt_cost = 0


class City(Terrain):
    def __init__(self, game, x, y, owner):
        super().__init__(game)     # the super init doesn't really do anything for now
        self.sprite = City_sprite(game, x, y, owner)
        self.name = "City"
        self.defense = 3
        self.type = BUILDING
        self.building_type = LAND
        self.hp = 20
        self.x = x
        self.y = y

        # every terrain class must define the mvt cost for all movement types
        # when a mvt_type cost is 0, it means units with this type of mvt cannot go on the tile
        self.infantry_mvt_cost = 1
        self.mech_mvt_cost = 1
        self.tires_mvt_cost = 1
        self.tread_mvt_cost = 1
        self.air_mvt_cost = 1
        self.ship_mvt_cost = 0
        self.transport_mvt_cost = 0
        self.owner = owner
        if owner is not None:
            self.owner.buildings.append(self)

    def add_funds(self):
        self.owner.funds += 1000

    def new_owner(self, player):
        self.owner.buildings.remove(self)
        self.sprite.kill()
        self.sprite = City_sprite(self.game, self.x, self.y, player)
        self.owner = player
        self.owner.buildings.append(self)



class Factory(Terrain):
    def __init__(self, game, x, y, owner):
        super().__init__(game)     # the super init doesn't really do anything for now
        self.sprite = Factory_sprite(game, x, y, owner)
        self.name = "factory"
        self.defense = 3
        self.type = BUILDING
        self.building_type = LAND
        self.hp = 20
        self.x = x
        self.y = y

        # every terrain class must define the mvt cost for all movement types
        # when a mvt_type cost is 0, it means units with this type of mvt cannot go on the tile
        self.infantry_mvt_cost = 1
        self.mech_mvt_cost = 1
        self.tires_mvt_cost = 1
        self.tread_mvt_cost = 1
        self.air_mvt_cost = 1
        self.ship_mvt_cost = 0
        self.transport_mvt_cost = 0
        self.owner = owner
        if owner is not None:
            self.owner.buildings.append(self)

    def add_funds(self):
        self.owner.funds += 1000

    def new_owner(self, player):
        self.owner.buildings.remove(self)
        self.sprite.kill()
        self.sprite = City_sprite(self.game, self.x, self.y, player)
        self.owner = player
        self.owner.buildings.append(self)


class HQ(Terrain):
    def __init__(self, game, x, y, owner):
        super().__init__(game)     # the super init doesn't really do anything for now
        self.sprite = Hq_sprite(game, x, y, owner)
        self.name = "HQ"
        self.defense = 4
        self.type = BUILDING
        self.building_type = LAND
        self.hp = 20
        self.x = x
        self.y = y

        # every terrain class must define the mvt cost for all movement types
        # when a mvt_type cost is 0, it means units with this type of mvt cannot go on the tile
        self.infantry_mvt_cost = 1
        self.mech_mvt_cost = 1
        self.tires_mvt_cost = 1
        self.tread_mvt_cost = 1
        self.air_mvt_cost = 1
        self.ship_mvt_cost = 0
        self.transport_mvt_cost = 0
        self.owner = owner
        if owner is not None:
            self.owner.buildings.append(self)

    def add_funds(self):
        self.owner.funds += 1000

    def new_owner(self, player):
        print("You win the game!")
        self.game.preview_text.text = ""
        self.game.preview_text.text = "You win the game!!!"
        self.game.draw()
        while 1:
            pass
