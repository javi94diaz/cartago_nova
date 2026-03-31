from game_core.actions.Action import Action
from game_core.Dice import Dice
from game_core.Enum import Faction
from game_core.Wall import Wall

class ShootAction(Action):
    def __init__(self, shooter, target):
        super().__init__()
        self.shooter = shooter
        self.target = target
        self.origin = shooter.zone
        self.destination = target.zone

        self.hit_rolls = []
        self.hits = {}

        self.save_rolls = []

        self.saved = 0

    def describe(self):
        return f"{self.shooter} -> {self.target}"

    def validate(self):

        print(f"[ShootAction:validate]")

        if self.shooter.type.shots == 0:
            raise ValueError(f"[ShootAction#{self.id}:validate] Unit cannot shoot")

        # if self.target.owner == self.shooter.owner:
        #     raise ValueError(f"[ShootAction:validate] Cannot shoot friendly unit")

        # if self.target.zone not in self.shooter.zone.adjacent:
        #     raise ValueError(f"[ShootAction:validate] Target not in range")

    def target_has_save_roll(self):
        
        return ( 
            self.target.owner.faction == Faction.CARTHAGE
            and self.target.zone.is_wall
            and self.target.zone.resistance > 0
            )

    def execute(self):
        
        self.validate()

        print(f"[ShootAction#{self.id}:execute] Shooter: {self.shooter} -->> Target: {self.target}")

        for shot in range (0, self.shooter.type.shots):

            if self.target.health <= 0 or self.target.zone is None:
                print(f"[ShootAction#{self.id}:execute] Target {self.target} is no longer alive. Shot lost.")
                break

            roll = Dice.d6()
            self.hit_rolls.append(roll)
            print(f"Shot {shot} from {self.shooter} throws D6 and gets: {roll}")

            if roll >= self.shooter.type.hit_number:
                print (f"Shooter {self.shooter} hits target {self.target}")

                if self.target not in self.hits:
                    self.hits[self.target] = 0
                
                self.hits[self.target] +=1
                print (f"[ShootAction#{self.id}:execute] self.hits = {self.hits}")
        # end for

        print(f"[ShootAction#{self.id}:execute] Unit {self.shooter} finished shooting against {self.target}")

    def apply_damage(self):

        for unit, damage in self.hits.items():

            if not unit.alive or unit.health <= 0 or unit.zone is None:
                print(f"[ShootAction#{self.id}:apply_damage] Target {unit} is no longer alive. Pending hits are lost.")
                continue

            final_damage = 0

            for i in range(damage):

                if self.target_has_save_roll():
                    print(f"Unit {unit} has save roll")
                    save_number = unit.zone.get_save_number()

                    roll = Dice.d6()
                    self.save_rolls.append(roll)

                    print(f"[ShootAction#{self.id}:apply_damage] {unit} attempts wall save: rolled {roll} (needs {save_number})")

                    if roll >= save_number:
                        print(f"[ShootAction#{self.id}:execute] {unit} saved the hit!")
                    else:
                        print(f"[ShootAction#{self.id}:execute] Save failed")
                        final_damage += 1
                else:
                    final_damage +=1
            # end for
            unit.health -= final_damage
            print(f"[ShootAction#{self.id}:execute] Unit {unit} takes {final_damage} damage points")

            if unit.health <= 0:
                print(f"[ShootAction#{self.id}:execute] Unit {unit} dies from shots!")

                if unit.zone and unit in unit.zone.units:
                    unit.zone.units.remove(unit)

