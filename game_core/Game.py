from game_core.Enum import Faction
from game_core.TurnManager import TurnManager
from game_core.Tableboard import Tableboard
from game_core.Player import Player
from game_core.UnitType import UnitType
from game_core.Unit import Unit

class Game:
    def __init__(self):
        print("[Game] Start Game")
        self.board = Tableboard()
        self.players = [
            Player("Javi", Faction.ROME),
            Player("Diego", Faction.CARTHAGE)
        ]

        self.unit_types = {
            "Velites": UnitType("Velites", 1, 1, 0, False),
            "Princeps": UnitType("Princeps", 1, 1, 0, False),
            "Numidian": UnitType("Numidian", 1, 1, 0, False),
            "Iberian": UnitType("Iberian", 1, 1, 0, False)
        }

        # TODO: leer de un archivo las unidades iniciales
        self.initial_units = {
            self.unit_types["Velites"]: 5,
            self.unit_types["Princeps"]: 7,
            self.unit_types["Numidian"]: 4,
            self.unit_types["Iberian"]: 2
        }

        self.units = []
        self.create_initial_units()
        self.turn_manager = TurnManager(self.players)


    def create_unit(self, unit_type, number, owner_player, zone):
        print (f"[Game:create_unit] Creating {number} {unit_type.name}/s")
        for num in range(0, number):
            self.units.append(
                Unit(unit_type, owner_player, zone)
            )
            
    def create_initial_units(self):
    
        for unit_type, number in self.initial_units.items():
            self.create_unit(unit_type, number, self.players[0], self.board.zones["Campamento"])
