import random
import json
from game_core.Enum import Faction, Phase
from game_core.TurnManager import TurnManager
from game_core.Board import Board
from game_core.Player import Player
from game_core.UnitType import UnitType
from game_core.Unit import Unit

class Game:
    def __init__(self):
        print("[Game:__init__] Start Game")
        self.board = Board()

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

        self.initial_units = []
        self.load_initial_units("resources/initial_units.json")

        self.units = []
        self.create_initial_units()

        # TODO: Load event cards from JSON file
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

        #self.event_cards = {}
        #self.load_event_cards()

        self.event_cards = {
            "Event 1": "Effect 1",
            "Event 2": "Effect 2",
            "Event 3": "Effect 3"
        }

        self.initial_event_cards = self.event_cards.copy()

        self.turn_manager = TurnManager(self.players)

        self.main_loop()

    def load_initial_units(self, filename):
        
        with open(filename, "r", encoding="utf-8") as file:
            filedata = json.load(file)

        for fileunit in filedata["initial_units"]:
            type = fileunit["type"]
            count = fileunit["count"]
            faction = fileunit["faction"]
            zone = fileunit["zone"]

            self.initial_units.append(
                {
                    "type": type,
                    "count": count,
                    "faction": faction,
                    "zone": zone
                }
            )

        print("[Game:load_initial_units] Loaded initial units")
        print (self.initial_units)

    def create_initial_units(self):

        for unit_data in self.initial_units:

            unit_type = self.unit_types[unit_data["type"]]
            count = unit_data["count"]

            try:
                faction = Faction[unit_data["faction"]]
            except KeyError:
                raise ValueError(f"Unknown faction: {unit_data['faction']}")
            
            player = self.get_player_by_faction(faction)
            zone = self.board.zones[unit_data["zone"]]

            self.create_unit(unit_type, count, player, zone)

    def create_unit(self, unit_type, count, owner_player, zone):
        print (f"[Game:create_unit] Creating {count} {unit_type.name}/s for {owner_player.faction} in {zone.name}")
        
        for _ in range(count):
            
            unit = Unit(unit_type, owner_player, zone)

            self.units.append(unit)
            zone.units.append(unit)
            owner_player.units.append(unit)
    
    def get_player_by_faction(self, faction):
        for player in self.players:
            if player.faction == faction:
                return player
        raise ValueError(f"No player found for faction {faction}")

    def resolve_initiative(self):
        
        user_input = None
        while (user_input != "yes" and user_input != "no"):
            print (f"[Game:resolve_initiative] {self.turn_manager.initiative_player}: Maintain initiative?: ")
            user_input = input()
        
        if user_input == "yes":
            print (f"[Game:resolve_initiative] {self.turn_manager.initiative_player} maintains initiative")

        elif user_input == "no":
            if self.turn_manager.initiative_player == self.players[0]:
                self.turn_manager.initiative_player = self.players[1]
                print (f"[Game:resolve_initiative] {self.turn_manager.initiative_player} gets initiative")

            elif self.turn_manager.initiative_player == self.players[1]:
                self.turn_manager.initiative_player = self.players[0]
                print (f"[Game:resolve_initiative] {self.turn_manager.initiative_player} gets initiative")

    def resolve_event(self):
        
        if (len(self.event_cards) == 0):
            self.event_cards = self.initial_event_cards.copy()
            print("self.event_cards")
            print(self.event_cards)
            print("[Game:resolve_event] Shuffling the event cards into a new deck!")

        event_name = random.choice(list(self.event_cards.keys()))

        print (f"[Game:resolve_event] Picked event card: {event_name} with effect {self.event_cards[event_name]}")
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

            self.board.print_zones()
            
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

            self.turn_manager.next_phase()

        print("[Game:main_loop] Game over!")
            