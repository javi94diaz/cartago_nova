
class MoveAction:
    def __init__(self, unit, origin, destination):
        self.unit = unit
        self.origin = origin
        self.destination = destination

    def check_valid_destination():
        pass
        # casilla adyacente y sin enemigos
        # si el bando es cartago, no puede salir de la ciudad
        # si la zona origen es muralla norte, no puede ir a la laguna

    def check_enemy():
        pass
        # chequear si hay enemigo en el destino?

    def execute(self, game):
        pass