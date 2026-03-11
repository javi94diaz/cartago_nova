from game_core.actions.Action import Action
from game_core.Wall import Wall

class OilAction(Action):
    def __init__(self, wall):
        self.wall = wall

    def validate(self):
        if not isinstance(self.wall, Wall):
            raise ValueError("Selected zone is not a wall")
        
        if any(status=="heating" for status in self.wall.oil_charges):
            raise ValueError("This wall already has oil heating")

    def execute(self):
        self.validate()
        self.wall.heat_oil()
        print(f"Oil is now heating on {self.wall.name}")