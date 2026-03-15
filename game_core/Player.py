

class Player():
    def __init__(self, name, faction):
        print(f"[Player] Create player {name} of {faction}")
        self.name = name
        self.faction = faction
        self.units = []

    def __repr__(self):
        return f"<Player: {self.name} ({self.faction})>"
    
    def apply_damage(self, damage_points, units):
        
        remaining_damage = damage_points
        print(f"[Player:apply_damage] Applying {damage_points} damage points among {units}")
        
        for i, unit in enumerate(list(units)):

            print(f"[Player:apply_damage] Remaining damages to apply: {remaining_damage}/{damage_points}")

            # Last unit receives all remaining_damage
            if i == len(units) - 1:

                user_input = remaining_damage
                print(f"{unit} receives remaining {remaining_damage} damage automatically")

            else:

                while True:

                    try:

                        user_input = int(input(f"Enter number of damage points for unit {unit}: "))

                        if (0 <= user_input <= remaining_damage) and (user_input <= unit.health):
                            break
                        else:
                            print("Invalid input, please type again.")

                    except ValueError:
                        print("Invalid input, please type a number.")

            unit.health -= user_input
            remaining_damage -= user_input

            if unit.health <= 0:
                print(f"Unit {unit} dies in combat!")
                unit.alive = False
                #unit.zone = None # TODO: Revisar si interesa, o dejarlo para saber dónde ha muerto la unidad
                unit.zone.units.remove(unit)

            else:
                print(f"Unit {unit} takes {user_input} damage points")