
class Unit:
    def __init__(self, unit_type, owner, zone):
        self.owner = owner
        self.zone = zone
        self.has_moved = False

        self.health = unit_type.max_health
        self.current_health = unit_type.max_health
        
        self.engaged = False
        self.alive = True