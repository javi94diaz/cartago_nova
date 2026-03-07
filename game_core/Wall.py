from game_core.Zone import Zone

class Wall(Zone):
    def __init__(self, id, name, x, y, capacity, resistance, bonus_defense, is_city=True):
        super().__init__(id, name, x, y, capacity, is_city)
        self.resistance = resistance
        self.bonus_defense = bonus_defense
        self.oil_charges = []  # "heating" or "ready"

    def heat_oil(self):
        self.oil_charges.append("heating")

    def advance_oil(self):
        self.oil_charges = ["ready" if status=="heating" else status for status in self.oil_charges]

    def use_oil(self):
        ready_charges = self.oil_charges.count("ready")
        self.oil_charges = [status for status in self.oil_charges if status != "ready"]
        # Add combat effect!
        return ready_charges