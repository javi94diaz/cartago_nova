import random
from game_core.Enum import Faction, Phase
from game_core.TurnManager import TurnManager
from game_core.Tableboard import Tableboard
from game_core.Player import Player
from game_core.UnitType import UnitType
from game_core.Unit import Unit

class Game:
    def __init__(self):
        print("[Game:__init__] Start Game")
        self.board = Tableboard()

        self.players = [
            Player("Javi", Faction.ROME),
            Player("Diego", Faction.CARTHAGE)
        ]

        self.unit_types = {
            "velites": UnitType("Velites", 1, 1, 0),
            "princeps": UnitType("Princeps", 1, 1, 0),
            "numidian": UnitType("Numidian", 1, 1, 0),
            "iberian": UnitType("Iberian", 1, 1, 0)
        }

        # TODO: leer de un archivo las unidades iniciales, a futuro se pueden poner varios escenarios
        self.initial_units = [
            {
                "type": "velites",
                "number": 5,
                "faction": Faction.ROME,
                "zone": "Campamento"
            },
            {
                "type": "princeps",
                "number": 7,
                "faction": Faction.ROME,
                "zone": "Campamento"
            },
            {
                "type": "numidian",
                "number": 4,
                "faction": Faction.CARTHAGE,
                "zone": "Muralla Este"
            },
            {
                "type": "iberian",
                "number": 2,
                "faction": Faction.CARTHAGE,
                "zone": "Muralla Sur"
            }
        ]

        self.units = []
        self.create_initial_units()

        # self.event_cards = {
        #     "Event 1": "Effect 1",
        #     "Event 2": "Effect 2",
        #     "Event 3": "Effect 3",
        #     "Event 4": "Effect 4",
        #     "Event 5": "Effect 5",
        #     "Event 6": "Effect 6",
        #     "Event 7": "Effect 7",
        #     "Event 8": "Effect 8",
        #     "Event 9": "Effect 9",
        #     "Event 10": "Effect 10",
        #     "Event 11": "Effect 11",
        #     "Event 12": "Effect 12",
        #     "Event 13": "Effect 13",
        #     "Event 14": "Effect 14",
        #     "Event 15": "Effect 15",
        #     "Event 16": "Effect 16"
        # }

        self.event_cards = {
            "Event 1": "Effect 1",
            "Event 2": "Effect 2",
            "Event 3": "Effect 3"
        }

        self.initial_event_cards = self.event_cards.copy()

        self.turn_manager = TurnManager(self.players)

        self.main_loop()

    def create_initial_units(self):

        for unit_data in self.initial_units:

            unit_type = self.unit_types[unit_data["type"]]
            number = unit_data["number"]
            player = self.get_player_by_faction(unit_data["faction"])
            zone = self.board.zones[unit_data["zone"]]

            self.create_unit(unit_type, number, player, zone)

    def create_unit(self, unit_type, number, owner_player, zone):
        print (f"[Game:create_unit] Creating {number} {unit_type.name}/s for {owner_player.faction} in {zone.name}")
        
        for _ in range(number):
            
            unit = Unit(unit_type, owner_player, zone)

            self.units.append(unit)
            zone.units.append(unit)
            owner_player.units.append(unit)

    def get_player_by_faction(self, faction):
        for player in self.players:
            if player.faction == faction:
                return player

    def resolve_initiative(self):
        
        user_input = None
        while (user_input != "yes" and user_input != "no"):
            print (f"[Game:resolve_initiative] Player {self.turn_manager.initiative_player}: Maintain initiative?: ")
            user_input = input()
        
        if user_input == "yes":
            print (f"[Game:resolve_initiative] Player {self.turn_manager.initiative_player} maintains initiative")

        elif user_input == "no":
            if self.turn_manager.initiative_player == self.players[0]:
                self.turn_manager.initiative_player = self.players[1]
                print (f"[Game:resolve_initiative] Player {self.turn_manager.initiative_player} gets initiative")

            elif self.turn_manager.initiative_player == self.players[1]:
                self.turn_manager.initiative_player = self.players[0]
                print (f"[Game:resolve_initiative] Player {self.turn_manager.initiative_player} gets initiative")
            

    def resolve_event(self):
        
        if (len(self.event_cards) == 0):
            self.event_cards = self.initial_event_cards.copy()
            print("self.event_cards")
            print(self.event_cards)
            print("[Game:resolve_event] Shuffling the event cards into a new deck!")

        event_name = random.choice(list(self.event_cards.keys()))

        print (f"[Game:resolve_event] Event card: {event_name}: with effect {self.event_cards[event_name]}")
        self.event_cards.pop(event_name)
        
        print("self.event_cards")
        print(self.event_cards)
        print("self.initial_event_cards")
        print (self.initial_event_cards)


    def resolve_oil_charges(self):
        print (f"[Game:resolve_oil_charges]")

    def resolve_move_and_assault(self):
        print (f"[Game:resolve_move_and_assault]")

    def resolve_shoot(self):
        print (f"[Game:resolve_shoot]")

    def resolve_combat(self):
        print (f"[Game:resolve_combat]")

    def main_loop(self):

        while (not self.turn_manager.game_over()):
            
            phase = self.turn_manager.phase
            
            if phase == Phase.INITIATIVE:
                self.resolve_initiative()

            elif phase == Phase.EVENT:
                self.resolve_event()

            elif phase == Phase.OIL_CHARGES:
                self.resolve_oil_charges()

            elif phase == Phase.MOVE_AND_ASSAULT:
                self.resolve_move_and_assault()

            elif phase == Phase.SHOOT:
                self.resolve_shoot()

            elif phase == Phase.COMBAT:
                self.resolve_combat()
            
            else:
                print(f"[Game:main_loop] Error - Phase not valid")

            self.turn_manager.next_phase()


            