
class UnitType:
    def __init__(self, name, max_health, combat_dice, shots, hit_number):
        self.name = name
        self.max_health = max_health        
        self.combat_dice = combat_dice
        self.shots = shots
        self.hit_number = hit_number

    def __repr__(self):
        return f"<UnitType {self.name}>"