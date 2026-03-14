
class Engagement():
    def __init__(self, zone):
        self.zone = zone
        self.units = zone.units.copy()
        self.attackers = []
        self.defenders = []

    def __repr__(self):
        return f"<Engagement {self.zone}>"
    
    def resolve(self): #TODO: sumar dados, hacer tiradas, aplicar modificadores, determinar ganador, aplicar daños
        
        print(f"Combat in {self.zone.name}")

        for unit in self.attackers:

            print(f"{unit} attacks!")

        for unit in self.defenders:

            print(f"{unit} defends!")
