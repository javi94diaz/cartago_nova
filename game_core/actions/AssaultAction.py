from game_core.actions.Action import Action
class AssaultAction(Action):
    def __init__(self, game, attacker, defender, origin, destination):
        pass

    def validate(self, game):
        pass

    def execute(self, game):
        pass

#El AssaultAction:
#Verifica que la zona destino es adyacente
#Verifica que hay enemigo
#Mueve la unidad
#Crea un Engagement
#Marca unidades como engaged
#Esto te dará claridad enorme.