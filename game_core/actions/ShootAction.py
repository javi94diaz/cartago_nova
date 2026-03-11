from game_core.actions.Action import Action
from game_core.Enum import Faction

class ShootAction(Action):
    def __init__(self, shooter, target):
        self.shooter = shooter
        self.target = target
        self.origin = shooter.zone
        self.destination = target.zone

        self.rolls = []
        self.hits = 0

    def validate(self, game):
        pass

    def execute(self, game):
        
        self.validate(game)

        print(f"[ShootAction:execute] Unit {self.shooter} shooted against {self.target}")