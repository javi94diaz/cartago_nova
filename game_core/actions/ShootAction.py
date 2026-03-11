from game_core.actions.Action import Action
from game_core.Enum import Faction

class ShootAction(Action):
    def __init__(self, shooter_unit, target_unit, origin, destination):
        self.shooter = shooter_unit
        self.target = target_unit
        self.origin = origin
        self.destination = destination

    def validate(self, game):
        pass

    def execute(self, game):
        
        self.validate(game)

        print(f"[ShootAction:execute] Unit {self.shooter} shooted against {self.target}")