from game_core.Dice import Dice

class Engagement():
    def __init__(self, zone):
        self.zone = zone
        self.units = zone.units.copy()
        self.attackers = []
        self.defenders = []

        self.attackers_rolls = []
        self.defenders_rolls = []

    def __repr__(self):
        return f"<Engagement {self.zone} between \n\t{self.attackers}\n\t{self.defenders}>"
    
    def roll_combat(self, units, group_name="Group"):

        # dice_num = sum(unit.type.combat_dice for unit in units)
        rolls = []
        for unit in units:

            print(f"{unit} fights!")

            unit_rolls = Dice.roll_many(unit.type.combat_dice)
            print(f"{unit} rolls: {unit_rolls}")

            rolls.extend(unit_rolls)

        print(f"[Engagement:roll_combat] {group_name} get {rolls} results in combat")
        return(rolls)

    def apply_damage(self, damage_points, units):
        
        remaining_damage = damage_points
        print(f"[Engagement:apply_damage] Applying {damage_points} damage points among {units}")
        
        for i, unit in enumerate(list(units)):

            print(f"[Engagement:apply_damage] Remaining damages to apply: {remaining_damage}/{damage_points}")

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

    def resolve(self):
        
        print(f"Combat in {self.zone.name}")

        print(f"[Engagement:resolve] ")
        self.attackers_rolls = self.roll_combat(self.attackers, "Attackers")
        self.defenders_rolls = self.roll_combat(self.defenders, "Defenders")

        if self.zone.is_wall:
            
            wall_bonus = self.zone.get_bonus_defense()
            print(f"[Engagement:resolve] Defender gets wall bonus: {wall_bonus}")
            self.defenders_rolls.append(wall_bonus)
            print(f"[Engagement:resolve] Defender final roll after bonus: {self.defenders_rolls}")


        attackers_success_num = sum(n >= 4 for n in self.attackers_rolls)
        defenders_success_num = sum(n >= 4 for n in self.defenders_rolls)
        
        # Apply damage
        units_damage = abs(attackers_success_num - defenders_success_num)

        print(f"[Engagement:resolve] Result - Attackers: {attackers_success_num} successes. Defenders: {defenders_success_num} successes")

        if attackers_success_num > defenders_success_num:  # TODO: distribuir daños entre las unidades
            print(f"[Engagement:resolve] Attacker wins! Defender takes {units_damage} damage point/s!")
            self.apply_damage(units_damage, self.defenders)
        elif attackers_success_num < defenders_success_num:
            print(f"[Engagement:resolve] Defender wins! Attacker takes {units_damage} damage point/s!")
            self.apply_damage(units_damage, self.attackers)
        else:
            print(f"[Engagement:resolve] Tie! Each side takes 1 damage point!")
            units_damage = 1
            self.apply_damage(units_damage, self.attackers)
            self.apply_damage(units_damage, self.defenders)

        # Apply wall damage
        attacker_6s = sum( n == 6 for n in self.attackers_rolls)
        defenders_6s = sum( n == 6 for n in self.defenders_rolls)

        if (self.zone.is_wall and attacker_6s > defenders_6s):

            print(f"[Engagement:resolve] Result - Attackers: {attacker_6s} 6-rolls. Defenders: {defenders_6s} 6-rolls")
            wall_damage = attacker_6s - defenders_6s
            print(f"[Engagement:resolve] {self.zone.name} wall takes {wall_damage} damage point/s!")

            self.zone.resistance -= wall_damage

            if self.zone.resistance < 0:
                print("[Engagement:resolve] Wall resistance is lower than 0, setting to 0")
                self.zone.resistance = 0

            print(f"[Engagement:resolve] {self.zone.name} wall has {self.zone.resistance} remaining resistance points")