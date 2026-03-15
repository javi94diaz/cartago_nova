from game_core.Dice import Dice

class Engagement():
    def __init__(self, zone):
        self.zone = zone
        self.units = zone.units.copy() # TODO: bug, se copia el estado del mundo demasiado pronto, y los disparos pueden matar unidades antes del combate
        self.attackers = []
        self.defenders = []

        self.attackers_rolls = []
        self.defenders_rolls = []

    def __repr__(self):
        return f"<Engagement {self.zone} between \n\t{self.attackers}\n\t{self.defenders}>"
    
    def get_combat_rolls(self, units, group_name="Group"):

        # dice_num = sum(unit.type.combat_dice for unit in units)
        rolls = []
        for unit in units:

            print(f"{unit} fights!")

            unit_rolls = Dice.roll_many(unit.type.combat_dice)
            print(f"{unit} rolls: {unit_rolls}")

            rolls.extend(unit_rolls)

        print(f"[Engagement:get_combat_rolls] {group_name} get {rolls} results in combat")
        return(rolls)

    def resolve(self):
        
        print(f"Combat in {self.zone.name}")

        print(f"[Engagement:resolve] ")
        self.attackers_rolls = self.get_combat_rolls(self.attackers, "Attackers")
        self.defenders_rolls = self.get_combat_rolls(self.defenders, "Defenders")

        if self.zone.is_wall:
            
            wall_bonus = self.zone.get_bonus_defense()
            print(f"[Engagement:resolve] Defender gets wall bonus: {wall_bonus}")
            self.defenders_rolls+=wall_bonus
            print(f"[Engagement:resolve] Defender final roll after bonus: {self.defenders_rolls}")


        attackers_success_num = sum(n >= 4 for n in self.attackers_rolls)
        defenders_success_num = sum(n >= 4 for n in self.defenders_rolls)
        
        # Apply damage
        units_damage = abs(attackers_success_num - defenders_success_num)

        print(f"[Engagement:resolve] Result - Attackers: {attackers_success_num} successes. Defenders: {defenders_success_num} successes")

        attacker_player = self.attackers[0].owner
        defender_player = self.defenders[0].owner

        if attackers_success_num > defenders_success_num:
            print(f"[Engagement:resolve] Attacker wins! Defender takes {units_damage} damage point/s!")
            defender_player.apply_damage(units_damage, self.defenders)

        elif attackers_success_num < defenders_success_num:
            print(f"[Engagement:resolve] Defender wins! Attacker takes {units_damage} damage point/s!")
            attacker_player.apply_damage(units_damage, self.attackers)

        else:
            print(f"[Engagement:resolve] Tie! Each side takes 1 damage point!")
            units_damage = 1
            attacker_player.apply_damage(units_damage, self.attackers)
            defender_player.apply_damage(units_damage, self.defenders)

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