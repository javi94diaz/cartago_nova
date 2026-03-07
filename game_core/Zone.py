
class Zone:
    def __init__(self, name):
        print(f"[Zone] Create Zone {name}")
        self.name = name
        self.units = []
        self.adjacent = set()   # Neighbor zones

    def __repr__(self):
        return f"<Zone {self.name}>"