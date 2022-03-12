class SolveTracker():

    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.turn_no_history = []


    def submit(self, finished_game):
        if finished_game.state == "win":
            self.wins += 1
        if finished_game.state == "loss":
            self.losses += 1
        self.turn_no_history.append(finished_game.turn_no)
      

    def get_stats(self):
        data = {}
        data["win_rate"] = f'{self.wins} / {(self.wins + self.losses)}'
        data["avg_turns"] = sum(self.turn_no_history) / len(self.turn_no_history)
        return data