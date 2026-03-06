
class UnitType:
    def __init__(self, name, max_health, attack, shots, can_shoot=False):
        self.name = name
        self.max_health = max_health        
        self.attack = attack
        self.shots = shots
        self.can_shoot = can_shoot
