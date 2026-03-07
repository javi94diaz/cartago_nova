from game_core.actions.Action import Action
from game_core.Enum import Faction
class MoveAction(Action):
    def __init__(self, unit, origin, destination):
        self.unit = unit
        self.origin = origin
        self.destination = destination

    def validate(self, game):
        if self.destination not in self.origin.adjacent and self.destination != self.origin:
            raise ValueError(f"[MoveAction:validate] Destination is not adjacent to origin")

        for unit in self.destination.units:
            #if unit.owner != self.unit.owner:
            if unit.zone == self.destination and unit.owner != self.unit.owner:
                raise ValueError(f"[MoveAction:validate] Enemy units present in destination")
            
        if self.unit.owner.faction == Faction.CARTHAGE:
            if self.origin.is_city and not self.destination.is_city:
                raise ValueError(f"[MoveAction:validate] Carthage cannot leave the city")
            
        if self.origin.id == "north_wall" and self.destination.id == "lagoon":
            raise ValueError("[MoveAction:validate] Cannot move from North Wall to Lagoon")

    def execute(self, game):
        
        self.validate(game)

        self.origin.units.remove(self.unit)
        self.destination.units.append(self.unit)

        self.unit.zone = self.destination