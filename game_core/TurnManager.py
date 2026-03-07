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

    def next_phase(self):
        print (f"[TurnManager:next_phase]")
        if self.phase == Phase.INITIATIVE:
            self.phase = Phase.EVENT

        elif self.phase == Phase.EVENT:
            self.phase = Phase.OIL_CHARGES

        elif self.phase == Phase.OIL_CHARGES:
            self.phase = Phase.MOVE_AND_ASSAULT

        elif self.phase == Phase.MOVE_AND_ASSAULT:
            self.phase = Phase.SHOOT

        elif self.phase == Phase.SHOOT:
            self.phase = Phase.COMBAT

        elif self.phase == Phase.COMBAT:
            self.phase = Phase.INITIATIVE

    
    def change_turn(self):
        pass        

    def game_over(self):
        pass
    
