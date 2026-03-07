from game_core.Enum import Phase

class TurnManager:
    def __init__(self, players):
        print(f"[TurnManager] Create TurnManager with {len(players)} players")
        self.turn = 0
        self.max_turns = 8
        self.players = players
        self.initiative_player = players[0]
        self.next_turn()

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
            self.next_turn()

    def next_turn(self):
        self.phase = Phase.INITIATIVE
        self.turn += 1
        if self.turn < 9:
            print(f"[TurnManager:next_turn] *********** Turn number: {self.turn}")

    def game_over(self):
        return self.turn > self.max_turns
