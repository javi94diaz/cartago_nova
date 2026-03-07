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
            "Velites": UnitType("Velites", 1, 1, 0),
            "Princeps": UnitType("Princeps", 1, 1, 0),
            "Numidian": UnitType("Numidian", 1, 1, 0),
            "Iberian": UnitType("Iberian", 1, 1, 0)
        }

        # TODO: leer de un archivo las unidades iniciales
        self.initial_units = [
            ("Velites", 5, Faction.ROME, "Campamento"),
            ("Princeps", 7, Faction.ROME, "Campamento"),
            ("Numidian", 4, Faction.CARTHAGE, "Muralla Este"),
            ("Iberian", 2, Faction.CARTHAGE, "Muralla Sur")
        ]

        self.units = []
        self.create_initial_units()
        self.turn_manager = TurnManager(self.players)


    def create_unit(self, unit_type, number, owner_player, zone):
        print (f"[Game:create_unit] Creating {number} {unit_type.name}/s")
        
        for _ in range(number):
            
            unit = Unit(unit_type, owner_player, zone)

            self.units.append(unit)
            zone.units.append(unit)
            owner_player.units.append(unit)

    def create_initial_units(self):
        for type_name, number, faction, zone_name in self.initial_units:

            unit_type = self.unit_types[type_name]
            player = self.get_player_by_faction(faction)
            zone = self.board.zones[zone_name]

            #print (self.board.zones["Campamento"])

            self.create_unit(unit_type, number, self.players[0], self.board.zones["Campamento"])

    def get_player_by_faction(self, faction):
        for player in self.players:
            if player.faction == faction:
                return player