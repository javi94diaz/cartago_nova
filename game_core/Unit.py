import uuid
class Unit:
    def __init__(self, unit_type, owner, zone):
        
        self.id = uuid.uuid4()
        
        self.type = unit_type
        self.owner = owner
        self.zone = zone
        self.health = unit_type.max_health
        self.current_health = unit_type.max_health
        # self.has_moved = False
        self.engaged = False
        self.alive = True


        