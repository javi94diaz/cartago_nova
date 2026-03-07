
class Zone:
    def __init__(self, name):
        print(f"[Zone] Create Zone {name}")
        self.name = name
        self.units = []
        #self.adjacent = set()   # Other Zone objects
        #self.units = []         # present units
        #####self.engagements = []   # Nota: solo puede haber un engagement por zona

    def __repr__(self):
        return f"<Zone {self.name}>"