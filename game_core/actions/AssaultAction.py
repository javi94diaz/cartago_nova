from game_core.actions.Action import Action
from game_core.Enum import Faction

class AssaultAction(Action):
    def __init__(self, unit, origin, destination):
        self.unit = unit
        self.origin = origin
        self.destination = destination

    def validate(self):
        if self.destination not in self.origin.adjacent and self.destination != self.origin:
            raise ValueError(f"[AssaultAction:validate] Destination is not adjacent to origin")
            
        enemy_found = False
        
        for unit in self.destination.units:
            if unit.owner != self.unit.owner:
                enemy_found = True
                break

        if not enemy_found:
            raise ValueError(f"[AssaultAction:validate] No enemy units in destination zone")

        if self.unit.engaged:
            raise ValueError(f"[AssaultAction:validate] Unit already engaged")

        if self.unit.owner.faction == Faction.CARTHAGE:
            if self.origin.is_city and not self.destination.is_city:
                raise ValueError(f"[AssaultAction:validate] Carthage cannot leave the city") # TODO: revisar esta condicion, posible bug
            
        if self.origin.id == "north_wall" and self.destination.id == "lagoon":
            raise ValueError("[AssaultAction:validate] Cannot move from North Wall to Lagoon")

    def execute(self):
        
        self.validate()

        # Move the units
        self.origin.units.remove(self.unit)
        self.destination.units.append(self.unit)

        self.unit.zone = self.destination
        
        print(f"[AssaultAction:execute] Unit {self.unit} assaulted {self.destination.name} zone")
        
        # Mark destination units as engaged
        for unit in self.destination.units:
            print(f"Unit {unit} is now engaged!")
            unit.engaged = True
            
        # crear Engagement!