from game_core.Enum import Faction
from game_core.TurnManager import TurnManager
from game_core.Tableboard import Tableboard
from game_core.Player import Player
from game_core.UnitType import UnitType
from game_core.Unit import Unit

class Game:
    def __init__(self):
        print("[Game:__init__] Start Game")
        self.board = Tableboard()

        print ("[Game:__init__] Vecinos")
        print (self.board.zones["Foro"].adjacent)

        self.players = [
            Player("Javi", Faction.ROME),
            Player("Diego", Faction.CARTHAGE)
        ]

        self.unit_types = {
            "Velites": UnitType("Velites", 1, 1, 0),
            "Princeps": UnitType("Princeps", 1, 1, 0),
            "Numidian": UnitType("Numidian", 1, 1, 0),
            "Iberian": UnitType("Iberian", 1, 1, 0)
        }

        # TODO: leer de un archivo las unidades iniciales, a futuro se pueden poner varios escenarios
        self.initial_units = [
            {
                "type": "Velites",
                "number": 5,
                "faction": Faction.ROME,
                "zone": "Campamento"
            },
            {
                "type": "Princeps",
                "number": 7,
                "faction": Faction.ROME,
                "zone": "Campamento"
            },
            {
                "type": "Numidian",
                "number": 4,
                "faction": Faction.CARTHAGE,
                "zone": "Muralla Este"
            },
            {
                "type": "Iberian",
                "number": 2,
                "faction": Faction.CARTHAGE,
                "zone": "Muralla Sur"
            }
        ]

        self.units = []
        self.create_initial_units()
        self.turn_manager = TurnManager(self.players)

    def create_initial_units(self):

        for unit_data in self.initial_units:

            unit_type = self.unit_types[unit_data["type"]]
            number = unit_data["number"]
            player = self.get_player_by_faction(unit_data["faction"])
            zone = self.board.zones[unit_data["zone"]]

            self.create_unit(unit_type, number, player, zone)

    def create_unit(self, unit_type, number, owner_player, zone):
        print (f"[Game:create_unit] Creating {number} {unit_type.name}/s")
        
        for _ in range(number):
            
            unit = Unit(unit_type, owner_player, zone)

            self.units.append(unit)
            zone.units.append(unit)
            owner_player.units.append(unit)

    def get_player_by_faction(self, faction):
        for player in self.players:
            if player.faction == faction:
                return player