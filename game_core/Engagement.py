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

        dice_num = 0
        for unit in units:

            print(f"{unit} fights!")
            dice_num += unit.type.combat_dice

        print(f"[Engagement:roll_combat] {group_name} roll {dice_num} dice")
        rolls = Dice.roll_many(dice_num)

        print(f"[Engagement:roll_combat] {group_name} get {rolls} results in combat")
        return(rolls)


    def resolve(self): #TODO: sumar dados, hacer tiradas, aplicar modificadores, determinar ganador, aplicar daños
        
        print(f"Combat in {self.zone.name}")

        print(f"[Engagement:resolve] ")
        self.attackers_rolls = self.roll_combat(self.attackers, "Attackers")
        self.defenders_rolls = self.roll_combat(self.defenders, "Defenders")

        attackers_success_num = sum(n >= 4 for n in self.attackers_rolls)
        defenders_success_num = sum(n >= 4 for n in self.defenders_rolls)
        units_damage = abs(attackers_success_num - defenders_success_num)

        print(f"[Engagement:resolve] Result - Attackers: {attackers_success_num} successes. Defenders: {defenders_success_num} successes")

        if attackers_success_num > defenders_success_num:  # TODO: distribuir daños entre las unidades
            print(f"[Engagement:resolve] Attacker wins! Defender takes {units_damage} damage point/s!")
        elif attackers_success_num < defenders_success_num:
            print(f"[Engagement:resolve] Defender wins! Attacker takes {units_damage} damage point/s!")
        else:
            print(f"[Engagement:resolve] Tie! Each side takes 1 damage point!")
            units_damage = 1

        attacker_6s = sum( n == 6 for n in self.attackers_rolls)
        defenders_6s = sum( n == 6 for n in self.defenders_rolls)

        if (self.zone.is_wall and attacker_6s > defenders_6s):

            print(f"[Engagement:resolve] Result - Attackers: {attacker_6s} 6-rolls. Defenders: {defenders_6s} 6-rolls")
            wall_damage = attacker_6s - defenders_6s
            print(f"[Engagement:resolve] {self.zone.name} wall takes {wall_damage} damage point/s!")

            self.zone.resistance -= wall_damage

            if self.zone.resistance < 0:
                print(f"MURO se queda negativo: {self.zone.resistance}")
                self.zone.resistance = 0
                print(f"MURO puesto a cero: {self.zone.resistance}")

            print(f"[Engagement:resolve] {self.zone.name} wall has {self.zone.resistance} remaining resistance points")