import json
from game_core.Zone import Zone
class Tableboard():
    def __init__(self):
        print(f"[Tableboard] Create Tableboard")
        
        self.zones = {}
        self.load_map("resources/map.json")
        self.print_zones()

    def print_zones(self):
        for zone_name, zone in self.zones.items():
            print(zone_name)

    def load_map(self, filename):
        
        with open(filename, "r", encoding="utf-8") as file:
            filedata = json.load(file)

        # Load zones
        for filezone in filedata["zones"]:
            name = filezone["name"]
            self.zones[name] = Zone(name)

        #Load adjacents
        for filezone in filedata["zones"]:
            zone = self.zones[filezone["name"]]

            for neighbor_name in filezone["adjacent"]:
                neighbor = self.zones[neighbor_name]
                zone.adjacent.add(neighbor) # Add neighbor to class set
                neighbor.adjacent.add(zone) # Bidirectional relationship