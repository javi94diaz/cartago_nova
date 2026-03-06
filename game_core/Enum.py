from enum import Enum

class Phase(Enum):
    INITIATIVE = 1
    EVENT = 2
    OIL_CHARGES = 3
    MOVE_AND_ASSAULT = 4
    SHOOT = 5
    COMBAT = 6

class Faction:
    ROME = 1
    CARTHAGE = 2
    NO_FACTION = 3
