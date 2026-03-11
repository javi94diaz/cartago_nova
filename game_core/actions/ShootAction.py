from game_core.actions.Action import Action
from game_core.Dice import Dice

class ShootAction(Action):
    def __init__(self, shooter, target):
        self.shooter = shooter
        self.target = target
        self.origin = shooter.zone
        self.destination = target.zone

        self.rolls = []
        self.hits = {}

    def __repr__(self):
        return f"<ShootAction {self.shooter} {self.target}>"

    def validate(self):

        print(f"[ShootAction:validate]")

    def execute(self):
        
        self.validate()

        print(f"[ShootAction:execute] Shooter: {self.shooter} | Target: {self.target}")

        for shot in range (0, self.shooter.type.shots):

            roll = Dice.d6()
            print(f"Shot {shot} from {self.shooter} throws D6 and gets: {roll}")

            if roll >= self.shooter.type.hit_number:
                print (f"Shooter {self.shooter} hits target {self.target}")

                if self.target not in self.hits:
                    self.hits[self.target] = 0
                
                self.hits[self.target] +=1
        # end for

        print(f"[ShootAction:execute] Unit {self.shooter} shooted against {self.target}")

    def apply_damage(self):

        for unit, damage in self.hits.items():

            unit.health -= damage
            print(f"Unit {unit} takes {damage} damage points")

            if unit.health <= 0:
                print(f"Unit {unit} dies from shots!")
                unit.alive = False
                #unit.zone = None # TODO: Revisar si interesa, o dejarlo para saber dónde ha muerto la unidad
                unit.zone.units.remove(unit)
