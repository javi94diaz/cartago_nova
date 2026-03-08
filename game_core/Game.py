import os
import random
import json
from game_core.Enum import Faction, Phase
from game_core.TurnManager import TurnManager
from game_core.Board import Board
from game_core.Player import Player
from game_core.UnitType import UnitType
from game_core.Unit import Unit
from game_core.EventCard import EventCard
from game_core.actions.MoveAction import MoveAction
from game_core.actions.OilAction import OilAction
from game_core.Wall import Wall

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

class Game:
    def __init__(self):
        print("[Game:__init__] Start Game")
        self.board = Board()

        self.players = [
            Player("Javi", Faction.ROME),
            Player("Diego", Faction.CARTHAGE)
        ]

        self.unit_types = {}
        self.load_unit_types("resources/unit_types.json")

        self.initial_units = []
        self.load_initial_units("resources/initial_units.json")

        self.units = []
        self.create_initial_units()

        self.event_cards = {}
        self.load_event_cards("resources/event_cards.json")

        self.initial_event_cards = self.event_cards.copy()

        self.turn_manager = TurnManager(self.players)

        self.main_loop()

    def load_unit_types(self, filename):

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        for key, unit_data in data["unit_types"].items():

            name = unit_data["name"]
            max_health = unit_data["max_health"]
            attack = unit_data["attack"]
            shots = unit_data["shots"]

            self.unit_types[key] = UnitType(name, max_health, attack, shots)

        print(f"[Game:load_unit_types] Loaded {len(self.unit_types)} unit types")
        # for key, value in self.unit_types.items():
        #     print (key, value)

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

        print(f"[Game:load_initial_units] Loaded {len(self.initial_units)} initial units")
        # for unit in self.initial_units:
        #     print (unit, end = "\n")

    def create_initial_units(self):

        for unit_data in self.initial_units:

            unit_type = self.unit_types[unit_data["type"]]
            count = unit_data["count"]

            try:
                faction = Faction[unit_data["faction"]]
            except KeyError:
                raise ValueError(f"[Game:create_initial_units] Unknown faction: {unit_data['faction']}")

            player = self.get_player_by_faction(faction)
            zone_id = unit_data["zone"]

            try:
                zone = self.board.zones[zone_id]
            except KeyError:
                raise ValueError(f"[Game:create_initial_units] Unknown zone: {zone_id}")

            self.create_unit(unit_type, count, player, zone)


    def create_unit(self, unit_type, count, owner_player, zone):
        print (f"[Game:create_unit] Creating {count} {unit_type.name}/s for {owner_player.faction} in {zone.name}")
        
        for _ in range(count):
            
            unit = Unit(unit_type, owner_player, zone)

            self.units.append(unit)
            zone.units.append(unit)
            owner_player.units.append(unit)
    
    def load_event_cards(self, filename):

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        self.event_cards = {}

        for card_id, card_data in data["event_cards"].items():

            title = card_data["title"]
            effect = card_data["effect"]

            card = EventCard(card_id, title, effect)

            self.event_cards[card_id] = card

        print(f"[Game:load_event_cards] Loaded {len(self.event_cards)} event cards")
        for key, value in self.event_cards.items():
            print (key, value)

    def get_player_by_faction(self, faction):
        for player in self.players:
            if player.faction == faction:
                return player
        raise ValueError(f"[Game:get_player_by_faction] No player found for faction {faction}")

    def choose_destination(self, unit):
        print(f"[Game:choose_destination]")
        print(f"Unit: {unit} - Choose a zone to move to: ")
        zones_list = list(self.board.zones.values())
        
        for i, zone in enumerate(zones_list):
            
            if zone == unit.zone:
                marker = "<- (HERE)" 
            elif zone in unit.zone.adjacent:
                marker = "-> (adjacent)"
            else:
                marker = ""
            print(f"{i}: {zone} {marker}")
        
        while True:
            try:
                user_input = int(input("Enter the number of your destination: "))
                if 0 <= user_input < len(zones_list):
                    destination = zones_list[user_input]

                    if destination not in unit.zone.adjacent and destination != unit.zone:
                        print ("Zone not valid. Please choose an adjacent zone.")
                        continue

                    return destination
                else:
                    print("Invalid number, please type again.")
            except ValueError:
                print("Invalid input, please type a number.")

    def choose_wall(self):
        print(f"[Game:choose_wall]")
        print(f"Choose a wall to heat oil into: ")
        zones_list = list(self.board.zones.values())
        wall_list = []
        for zone in zones_list:
            if isinstance(zone, Wall):
                wall_list.append(zone)

        for i, wall in enumerate(wall_list):
            print(f"{i}: {wall.name} {wall.oil_charges}")
        
        while True:
            try:
                user_input = int(input("Enter the number of a wall: "))
                if 0 <= user_input < len(wall_list):
                    destination = wall_list[user_input]
                    action = OilAction(destination)
                    action.validate(self)
                    return destination
                    
                else:
                    print("Invalid number, please type again.")
            except ValueError:
                print("Invalid input, please type a number.")
            except Exception as e:
                print(f"Cannot select this wall: {e}")

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
            for key, value in self.event_cards.items():
                print(key, value)
            print("[Game:resolve_event] Shuffling the event cards into a new deck!")

        event_name = random.choice(list(self.event_cards.keys()))

        print (f"[Game:resolve_event] Picked event card: {event_name} with effect {self.event_cards[event_name]}")
        self.event_cards.pop(event_name)
        
        print(f"{len(self.event_cards)}/{len(self.initial_event_cards)} event cards remaining")


    def resolve_oil_charges(self):
        print("[Game:resolve_oil_charges]")

        for zone in self.board.zones.values():
            if isinstance(zone, Wall):
                zone.advance_oil()

        wall = self.choose_wall()
        action = OilAction(wall)

        try:
            action.execute(self)
            print(f"{wall.name}: {wall.oil_charges}")
        except Exception as e:
            print(f"[Game:resolve_oil_charges] Error adding oil charges: {e}")


 
    def resolve_move_and_assault(self):
        print (f"[Game:resolve_move_and_assault]")

        print (f"[Game:resolve_move_and_assault] {self.turn_manager.initiative_player} Move Step")

        for unit in self.units:

            destination = self.choose_destination(unit)
            action = MoveAction(unit, unit.zone, destination)

            try:
                action.execute(self)
            except ValueError as err:
                print(f"[Game:resolve_move_and_assault] Invalid move {err}")

    def resolve_shoot(self):
        print (f"[Game:resolve_shoot]")

    def resolve_combat(self):
        print (f"[Game:resolve_combat]")

    def main_loop(self):

        while (not self.turn_manager.game_over()):

            #clear_screen()
            phase = self.turn_manager.phase
            print(f"[Game:main_loop] Phase: {phase}")
            
            #self.board.print_zone_basic()
            self.board.print_zone_summary()
            #self.board.print_zone_detailed()
            
            if phase == Phase.INITIATIVE: # [OK] DONE
                #self.resolve_initiative()
                pass

            elif phase == Phase.EVENT: # [OK] DONE
                #self.resolve_event()
                pass

            elif phase == Phase.OIL_CHARGES: # [OK] DONE
                self.resolve_oil_charges()
                pass 

            elif phase == Phase.MOVE_AND_ASSAULT:
                #self.resolve_move_and_assault()
                pass # TODO: move first initiative player's units

            elif phase == Phase.SHOOT:
                #self.resolve_shoot()
                pass

            elif phase == Phase.COMBAT:
                #self.resolve_combat()
                pass

            self.turn_manager.next_phase()

        print("[Game:main_loop] Game over!")
            