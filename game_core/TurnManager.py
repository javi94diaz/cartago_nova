from game_core.Enum import Phase

class TurnManager:
    def __init__(self, players):
        print(f"[TurnManager] Create TurnManager with {len(players)} players")
        self.turn = 1
        self.max_turns = 8
        self.players = players
        self.current_player = players[0]
        self.initiative_player = players[0]
        self.phase = Phase.INITIATIVE

    def change_phase(self):
        pass    
    
    def change_turn(self):
        pass        

    def game_over(self):
        pass
    
