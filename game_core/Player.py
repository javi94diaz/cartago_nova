

class Player():
    def __init__(self, name, faction):
        print(f"[Player] Create player {name} of {faction}")
        self.name = name
        self.faction = faction
        self.units = []
