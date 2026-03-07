import json
from game_core.Zone import Zone
from game_core.Wall import Wall
from game_core.Enum import Faction

class Board():
    def __init__(self):
        print(f"[Board] Create Board")
        
        self.zones = {}
        self.load_map("resources/map.json")
        #self.print_zones()

    def load_map(self, filename):

        with open(filename, "r", encoding="utf-8") as file:
            filedata = json.load(file)

        # Load and create zones
        for zone_id, filezone in filedata["zones"].items():
            
            if filezone.get("is_wall"):
                name = filezone["name"]
                x = filezone["x"]
                y = filezone["y"]
                capacity = filezone["capacity"]
                is_city = filezone["is_city"]
                is_wall = filezone["is_wall"]
                resistance = filezone["resistance"]
                bonus_defense = filezone["bonus_defense"]

                self.zones[zone_id] = Wall(zone_id, name, x, y, capacity, resistance, bonus_defense, is_city)
            else:
                name = filezone["name"]
                x = filezone["x"]
                y = filezone["y"]
                capacity = filezone["capacity"]
                is_city = filezone["is_city"]

                self.zones[zone_id] = Zone(zone_id, name, x, y, capacity, is_city)

        # Load adjacents
        for zone_id, filezone in filedata["zones"].items():
            zone = self.zones[zone_id]

            for neighbor_id in filezone["adjacent"]:
                neighbor = self.zones[neighbor_id]
                zone.adjacent.add(neighbor)
                neighbor.adjacent.add(zone)  # Bidirectional relationship
        
        print("[Board:load_map] Loaded map")

    def print_zone_basic(self):
        print("[Board:print_zones]")
        for zone_name, zone in self.zones.items():
            print(f"Zone {zone_name} has {len(zone.units)} unit/s")
            
            for unit in zone.units:
                print (f" {unit}")

    def print_zone_summary(self):

        print("\n ==== BOARD STATE SUMMARY ====")
        print(f"{'Zone':18} {'ROME':>6} {'CARTHAGE':>10}")
        print("-" * 36)

        for zone in self.zones.values():

            rome = 0
            carthage = 0

            for unit in zone.units:
                if unit.owner.faction == Faction.ROME:
                    rome += 1
                elif unit.owner.faction == Faction.CARTHAGE:
                    carthage += 1

            print(f"{zone.name:18} {rome:>6} {carthage:>6}")


    def print_zone_detailed(self):
        print("\n=== BOARD STATE DETAILED ===\n")
        for zone in self.zones.values():
            print(f"Zone: {zone.name}")

            faction_units = {}
            for unit in zone.units:
                fac = unit.owner.faction
                if fac not in faction_units:
                    faction_units[fac] = {}
                utype = unit.type.name
                if utype not in faction_units[fac]:
                    faction_units[fac][utype] = 0
                faction_units[fac][utype] += 1

            for fac, units in faction_units.items():
                units_str = ", ".join([f"{utype} x{count}" for utype, count in units.items()])
                print(f"  {fac.name}: {units_str}")

            if not faction_units:
                print("  No units")
            
            print()