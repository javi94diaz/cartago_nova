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
from game_core.Engagement import Engagement
from game_core.actions.OilAction import OilAction
from game_core.actions.MoveAction import MoveAction
from game_core.actions.AssaultAction import AssaultAction
from game_core.actions.ShootAction import ShootAction
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

        self.engagements = []

        self.main_loop()

    def load_unit_types(self, filename):

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        for key, unit_data in data["unit_types"].items():

            name = unit_data["name"]
            max_health = unit_data["max_health"]
            attack = unit_data["attack"]
            shots = unit_data["shots"]
            hit_number = unit_data.get("hit_number", 7) # Optional, 7 if not found in JSON

            self.unit_types[key] = UnitType(name, max_health, attack, shots, hit_number)

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

    def choose_wall(self):
        print(f"[Game:choose_wall]")
        print(f"Choose a wall to heat oil into: ")
        zones_list = list(self.board.zones.values())
        wall_list = []
        for zone in zones_list:
            if isinstance(zone, Wall):
                wall_list.append(zone)

        for i, wall in enumerate(wall_list):
            print(f"\t{i}: {wall.name} {wall.oil_charges}")
        
        while True:
            try:
                user_input = int(input("Enter the number of a wall: "))
                if 0 <= user_input < len(wall_list):
                    destination = wall_list[user_input]
                    action = OilAction(destination)
                    action.validate()
                    return destination
                    
                else:
                    print("Invalid number, please type again.")
            except ValueError:
                print("Invalid input, please type a number.")
            except Exception as e:
                print(f"Cannot select this wall: {e}")

    def get_other_player(self, initiative_player):
        for player in self.players:
            if player != initiative_player:
                return player

    def zone_has_enemy_units(self, zone, player):

        for unit in zone.units:
            if unit.owner != player:
                return True

        return False

    def choose_move_destination(self, unit):
        print(f"[Game:choose_move_destination]  =============== MOVE =================")
        print(f"Unit: {unit} - Choose a zone to move to: ")
        zones_list = list(self.board.zones.values())
        
        for i, zone in enumerate(zones_list):
            
            if zone == unit.zone:
                marker = "<--------------- (HERE)" 
            elif zone in unit.zone.adjacent:
                marker = "-> (adjacent)"
            else:
                marker = ""
            print(f"\t{i}: {zone} {marker}")
        print("ENTER - Stay in current area")
        
        while True:
            try:
                user_input = input("Enter the number of your destination: ")
                
                if user_input == "":
                    return unit.zone # Stay in the same zone

                user_input = int(user_input)

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

    def move_units_for_player(self, player):
        
        units_capable_of_moving = [unit for unit in player.units if unit.alive and not unit.engaged]
        print(f"Units capable of moving:\n {units_capable_of_moving}")

        for unit in units_capable_of_moving:

            while True:
                origin = unit.zone
                destination = self.choose_move_destination(unit)
                action = MoveAction(unit, origin, destination)

                try:
                    action.execute()
                    break
                except ValueError as err:
                    print(f"[Game:move_units_for_player] Invalid move {err}. Choose another destination.")

    def choose_assault_destination(self, unit, player):
        print(f"[Game:choose_assault_destination] =============== ASSAULT =================")
        print(f"Unit: {unit} - Choose a zone to assault: ")
        zones_list = list(self.board.zones.values())

        for i, zone in enumerate(zones_list):
            
            if zone == unit.zone:
                marker = "<--------------- (HERE)" 
            elif self.zone_has_enemy_units(zone, player):
                marker = "-> (enemies)"
            else:
                marker = ""
            print(f"\t{i}: {zone} {marker}")
        print("ENTER - Skip assault")

        while True:
            try:
                
                user_input = input("Enter the number of the zone to assault: ")
                
                if user_input == "":
                    return unit.zone # Skip assault

                user_input = int(user_input)
                
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

    def assault_units_for_player(self, player):
        
        units_capable_of_assaulting = [unit for unit in player.units if unit.alive and not unit.engaged]
        print(f"Units capable of assaulting:\n {units_capable_of_assaulting}")

        for unit in units_capable_of_assaulting:

            while True:
                origin = unit.zone
                destination = self.choose_assault_destination(unit, player)

                if destination != origin:

                    action = AssaultAction(unit, origin, destination)

                    try:
                        action.execute()
                        break
                    except ValueError as err:
                        print(f"[Game:assault_units_for_player] Invalid assault {err}. Choose another destination.")
                else:
                    print (f"Unit {unit} skipped assault")
                    break

    def create_engagements(self):
        
        self.engagements = []

        for zone in self.board.zones.values():

            factions = set(unit.owner.faction for unit in zone.units)

            if len(factions) > 1:

                engagement = Engagement(zone)

                for unit in zone.units:

                    if unit.owner.faction == Faction.ROME:
                        engagement.attackers.append(unit)
                    else:
                        engagement.defenders.append(unit)

                self.engagements.append(engagement)

                print(f"Engagement created! {engagement}")

    def select_shoot_targets(self, player_1, player_2):
        
        shoot_actions = []

        shooters = [unit for unit in player_1.units if unit.alive and unit.type.shots > 0]
        print(f"\n[Game:select_shoot_targets] Shooters for player {player_1} are {shooters}")

        for shooter in shooters:
            
            # Targets: alive enemies in shooter's zone or adjacent zones
            targets = [
                unit for unit in player_2.units
                if unit.alive and (unit.zone == shooter.zone or unit.zone in shooter.zone.adjacent)
            ]
            
            if not targets:
                print(f"[Game:select_shoot_targets] Shooter {shooter} has no targets on sight")
                continue

            print(f"Targets found: {targets}")

            for i, target in enumerate(targets):
                print(f"\t{i}: {target} ({target.zone})")

            while True:
                try:
                    user_input = input(f"Enter target unit number for {shooter} (Enter to skip): ")
                    
                    if user_input == "":
                        print (f"Unit {shooter} skipped shooting.")
                        break

                    user_input = int(user_input)

                    if 0 <= user_input < len(targets):
                        target = targets[user_input]
                        print(f"Target selected: {target}")
                        shoot_actions.append(ShootAction(shooter, target))
                        print(f"Added shoot action:\n\t {(shooter, target)}")
                        break
                    else:
                        print("Invalid number, please type again.")
                except ValueError:
                    print("Invalid input, please type a number.")
            # end while
        # end for
        return shoot_actions

    def resolve_initiative_phase(self):
        
        print("[Game:resolve_initiative] ====== INITIATIVE ======")

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

    def resolve_event_phase(self):

        print("[Game:resolve_event] ====== EVENT ======")

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

    def resolve_oil_charges_phase(self):

        print("[Game:resolve_oil_charges] ====== OIL CHARGES ======")

        for zone in self.board.zones.values():
            if isinstance(zone, Wall):
                zone.advance_oil()

        wall = self.choose_wall()
        action = OilAction(wall)

        try:
            action.execute()
            print(f"{wall.name}: {wall.oil_charges}")
        except Exception as e:
            print(f"[Game:resolve_oil_charges] Error adding oil charges: {e}")

    def resolve_move_and_assault_phase(self):

        print (f"[Game:resolve_move_and_assault] ====== MOVE AND ASSAULT ======")

        initiative_player = self.turn_manager.initiative_player
        other_player = self.get_other_player(initiative_player)

        self.move_units_for_player(initiative_player)
        self.assault_units_for_player(initiative_player)
        self.move_units_for_player(other_player)
        self.assault_units_for_player(other_player)

    def resolve_shoot_phase(self):

        print (f"[Game:resolve_shoot] ====== SHOOT ======")

        initiative_player = self.turn_manager.initiative_player
        other_player = self.get_other_player(initiative_player)

        shoot_actions = self.select_shoot_targets(initiative_player, other_player)
        shoot_actions += self.select_shoot_targets(other_player, initiative_player)
    
        print(f"\n[Game:resolve_shoot_phase] Shoot actions")
        for action in shoot_actions:
            print(f"\t{action}")

        for action in shoot_actions:
            action.execute()

        for action in shoot_actions:
            action.apply_damage()

    def resolve_combat_phase(self):

        print (f"[Game:resolve_combat] ====== COMBAT ======")

        self.create_engagements()

        print(self.engagements)

        for engagement in self.engagements:
            engagement.resolve()


    def main_loop(self):

        while (not self.turn_manager.game_over()):

            #clear_screen()
            phase = self.turn_manager.phase
            print(f"[Game:main_loop] Phase: {phase}")
            
            #self.board.print_zone_basic()
            self.board.print_zone_summary()
            #self.board.print_zone_detailed()
            
            if phase == Phase.INITIATIVE: # [OK] DONE
                #self.resolve_initiative_phase()
                pass

            elif phase == Phase.EVENT: # [OK] DONE mas o menos
                #self.resolve_event_phase()
                pass

            elif phase == Phase.OIL_CHARGES: # [OK] DONE
                #self.resolve_oil_charges_phase()
                pass 

            elif phase == Phase.MOVE_AND_ASSAULT: # [OK] DONE
                self.resolve_move_and_assault_phase()
                pass

            elif phase == Phase.SHOOT: # [OK] DONE
                self.resolve_shoot_phase()
                pass

            elif phase == Phase.COMBAT: # [OK] DONE
                self.resolve_combat_phase()
                pass

            self.turn_manager.next_phase()

        print("[Game:main_loop] Game over!")
            