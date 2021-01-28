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

#TODO do a clean up, lots of info is now unused or redondant and this can be improved


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
        self.can_attack = None
        self.embarked = False
        self.ammo = None
        self.type = None

    def end_turn(self):
        if self.mvt_type == AIR or self.mvt_type == SHIP or self.mvt_type == TRANSPORT:
            self.fuel -= fuel_cost[self.type]
            if self.fuel < 1:
                return 1
        if self.available:
            self.available.kill()
            self.available = None
        return 0

    def new_turn(self):
        if self.embarked:
            return
        self.available = Available(self.game, self.x, self.y)

    def die(self):
        self.sprite.kill()
        if self.available:
            self.available.kill()

    def move(self, x, y):
        # print("I moved")
        self.x = x
        self.y = y
        self.sprite.rect.x = x * TILESIZE
        self.sprite.rect.y = y * TILESIZE
        if self.available:
            self.available.rect.x = x * TILESIZE
            self.available.rect.y = y * TILESIZE

    def highlight(self):
        self.available.kill()
        self.available = Select(self.game, self.x, self.y)

    def unhighlight(self):
        self.available.kill()
        self.available = Available(self.game, self.x, self.y)

    def embark(self):
        self.sprite.kill()
        self.embarked = True
        if self.available:
            self.available.kill()

    def drop(self, x, y):
        self.embarked = False
        if self.type == INFANTRY:
            self.sprite = Infantry_sprite(self.game, self.x, self.y, self.player.ID)
        elif self.type == MECH:
            self.sprite = Mech_sprite(self.game, self.x, self.y, self.player.ID)
        self.move(x, y)

    def refuel(self):
        self.ammo = max_ammo[self.type]
        self.fuel = max_fuel[self.type]

class Infantry(Unit):
    def __init__(self, player, game, x, y):
        super().__init__()  # the super init doesn't really do anything for now
        self.x = x
        self.y = y
        self.game = game
        self.player = player
        self.name = "Infantry"
        self.fuel = 99
        self.ammo = 0
        self.type = INFANTRY
        self.element = LAND
        self.movement = 3
        self.hp = 100
        self.mvt_type = INFANTRY      # All unit need a movement type, check settings for all movement types
        self.sprite = Infantry_sprite(game, x, y, self.player.ID)
        self.available = None
        self.can_attack = True


class Tank(Unit):
    def __init__(self, player, game, x, y):
        super().__init__()  # the super init doesn't really do anything for now
        self.x = x
        self.y = y
        self.game = game
        self.player = player
        self.name = "Tank"
        self.fuel = 70
        self.ammo = 9
        self.type = TANK
        self.element = LAND
        self.movement = 6
        self.hp = 100
        self.mvt_type = TREAD        # All unit need a movement type, check settings for all movement types
        self.sprite = Tank_sprite(game, x, y, self.player.ID)
        self.available = None
        self.can_attack = True


class Apc(Unit):
    def __init__(self, player, game, x, y):
        super().__init__()  # the super init doesn't really do anything for now
        self.x = x
        self.y = y
        self.game = game
        self.player = player
        self.name = "APC"
        self.fuel = 99
        self.ammo = 0
        self.type = APC
        self.element = LAND
        self.movement = 6
        self.hp = 100
        self.mvt_type = TREAD        # All unit need a movement type, check settings for all movement types
        self.sprite = APC_sprite(game, x, y, self.player.ID)
        self.available = None
        self.can_attack = False
        self.holding = None


class Artillery(Unit):
    def __init__(self, player, game, x, y):
        super().__init__()  # the super init doesn't really do anything for now
        self.x = x
        self.y = y
        self.game = game
        self.player = player
        self.name = "Artillery"
        self.fuel = 50
        self.ammo = 9
        self.type = ARTILLERY
        self.element = LAND
        self.range = (2, 3)
        self.movement = 5
        self.hp = 100
        self.mvt_type = TREAD        # All unit need a movement type, check settings for all movement types
        self.sprite = Artillery_sprite(game, x, y, self.player.ID)
        self.available = None
        self.can_attack = True


class Recon(Unit):
    def __init__(self, player, game, x, y):
        super().__init__()  # the super init doesn't really do anything for now
        self.x = x
        self.y = y
        self.game = game
        self.player = player
        self.name = "Recon"
        self.fuel = 80
        self.ammo = 0
        self.type = RECON
        self.element = LAND
        self.movement = 8
        self.hp = 100
        self.mvt_type = TIRES      # All unit need a movement type, check settings for all movement types
        self.sprite = Recon_sprite(game, x, y, self.player.ID)
        self.available = None
        self.can_attack = True


class Mech(Unit):
    def __init__(self, player, game, x, y):
        super().__init__()  # the super init doesn't really do anything for now
        self.x = x
        self.y = y
        self.game = game
        self.player = player
        self.name = "Mech"
        self.fuel = 70
        self.ammo = 3
        self.type = MECH
        self.element = LAND
        self.movement = 2
        self.hp = 100
        self.mvt_type = MECH      # All unit need a movement type, check settings for all movement types
        self.sprite = Mech_sprite(game, x, y, self.player.ID)
        self.available = None
        self.can_attack = True


class MDTank(Unit):
    def __init__(self, player, game, x, y):
        super().__init__()  # the super init doesn't really do anything for now
        self.x = x
        self.y = y
        self.game = game
        self.player = player
        self.name = "MDTank"
        self.fuel = 10 # 50
        self.ammo = 8
        self.type = MDTANK
        self.element = LAND
        self.movement = 5
        self.hp = 100
        self.mvt_type = TREAD      # All unit need a movement type, check settings for all movement types
        self.sprite = MDTank_sprite(game, x, y, self.player.ID)
        self.available = None
        self.can_attack = True


class Antiair(Unit):
    def __init__(self, player, game, x, y):
        super().__init__()  # the super init doesn't really do anything for now
        self.x = x
        self.y = y
        self.game = game
        self.player = player
        self.name = "Antiair"
        self.fuel = 60
        self.ammo = 9
        self.type = ANTIAIR
        self.element = LAND
        self.movement = 6
        self.hp = 100
        self.mvt_type = TREAD      # All unit need a movement type, check settings for all movement types
        self.sprite = Antiair_sprite(game, x, y, self.player.ID)
        self.available = None
        self.can_attack = True


class Missiles(Unit):
    def __init__(self, player, game, x, y):
        super().__init__()  # the super init doesn't really do anything for now
        self.x = x
        self.y = y
        self.game = game
        self.player = player
        self.name = "Missiles"
        self.fuel = 50
        self.ammo = 6
        self.type = MISSILES
        self.element = LAND
        self.range = (3, 5)
        self.movement = 4
        self.hp = 100
        self.mvt_type = TIRES        # All unit need a movement type, check settings for all movement types
        self.sprite = Missiles_sprite(game, x, y, self.player.ID)
        self.available = None
        self.can_attack = True


class Rockets(Unit):
    def __init__(self, player, game, x, y):
        super().__init__()  # the super init doesn't really do anything for now
        self.x = x
        self.y = y
        self.game = game
        self.player = player
        self.name = "Rockets"
        self.fuel = 50
        self.ammo = 6
        self.type = ROCKETS
        self.element = LAND
        self.range = (3, 5)
        self.movement = 5
        self.hp = 100
        self.mvt_type = TIRES        # All unit need a movement type, check settings for all movement types
        self.sprite = Rockets_sprite(game, x, y, self.player.ID)
        self.available = None
        self.can_attack = True