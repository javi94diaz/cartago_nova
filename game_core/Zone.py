
class Zone:
    def __init__(self, zone_id, name, x , y, capacity, is_city):
        #print(f"[Zone] Create Zone {name}")
        self.id = zone_id
        self.name = name
        self.x = x
        self.y = y
        self.capacity = capacity
        self.is_city = is_city
        self.units = []
        self.adjacent = set()   # Neighbor zones

    def __repr__(self):
        return f"<Zone {self.name}>"