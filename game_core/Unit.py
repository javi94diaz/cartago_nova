import uuid
class Unit:
    
    _type_counters = {}
    
    def __init__(self, unit_type, owner, zone):
        
        self.id = uuid.uuid4()
        
        self.type = unit_type
        self.owner = owner
        self.zone = zone

        name = unit_type.name
        if name not in Unit._type_counters:
            Unit._type_counters[name] = 0

        Unit._type_counters[name] += 1
        self.number = Unit._type_counters[name]

        self.health = unit_type.max_health
        self.current_health = unit_type.max_health
        # self.has_moved = False
        self.engaged = False
        self.alive = True

    def __repr__(self):
        return f"<Unit {self.type.name}#{self.number} {self.owner.faction} @{self.zone.name}>"

        