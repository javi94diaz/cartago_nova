from game_core.Zone import Zone

class Wall(Zone):
    def __init__(self, id, name, x, y, capacity, max_resistance, bonus_defense, is_wall, is_city=True):
        super().__init__(id, name, x, y, capacity, is_city)
        self.max_resistance = max_resistance
        self.resistance = max_resistance
        self.bonus_defense = bonus_defense
        self.oil_charges = []  # "heating" or "ready"
        self.is_wall = is_wall

    def get_save_number(self):

        if self.resistance == 3:
            return 4
        elif self.resistance == 2:
            return 5
        elif self.resistance == 1:
            return 6
        else:
            return None

    def get_bonus_defense(self):

        if self.resistance == 3:
            return [6, 4, 4]
        elif self.resistance == 2:
            if self.id == "south_wall":
                return [6,4]
            elif self.id == "east_wall":
                return [4,4]
            else:
                print(f"[Wall:get_bonus_defense] Error getting bonus")
                raise ValueError
        elif self.resistance == 1:
            if self.id == "north_wall":
                return [6]
            else:
                return [4]
        else:
            return None

    def heat_oil(self):
        self.oil_charges.append("heating")

    def advance_oil(self):
        self.oil_charges = ["ready" if status=="heating" else status for status in self.oil_charges]

    def use_oil(self):
        ready_charges = self.oil_charges.count("ready")
        self.oil_charges = [status for status in self.oil_charges if status != "ready"]
        # Add combat effect!
        return ready_charges
    
