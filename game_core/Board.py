import json
from game_core.Zone import Zone
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
        for filezone in filedata["zones"]:
            name = filezone["name"]
            x = filezone["x"]
            y = filezone["y"]
            capacity = filezone["capacity"]
            self.zones[name] = Zone(name, x, y, capacity)

        #Load adjacents
        for filezone in filedata["zones"]:
            zone = self.zones[filezone["name"]]

            for neighbor_name in filezone["adjacent"]:
                neighbor = self.zones[neighbor_name]
                zone.adjacent.add(neighbor) # Add neighbor to class set
                neighbor.adjacent.add(zone) # Bidirectional relationship

    def print_zones(self): # FIRST METHOD
        print("[Board:print_zones]")
        for zone_name, zone in self.zones.items():
            print(f"Zone {zone_name} has {len(zone.units)} unit/s")
            
            for unit in zone.units:
                print (f" {unit}")

    def print_zone_summary(self):

        print("\n ==== BOARD STATE ====")
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