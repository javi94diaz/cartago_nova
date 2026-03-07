
class Zone:
    def __init__(self, name, x , y, capacity):
        print(f"[Zone] Create Zone {name}")
        self.name = name
        self.x = x
        self.y = y
        self.capacity = capacity
        self.units = []
        self.adjacent = set()   # Neighbor zones

    def __repr__(self):
        return f"<Zone {self.name}>"