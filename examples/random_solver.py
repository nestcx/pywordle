from pywordle.pywordle import Wordle
import random


class SolveTracker():

    def __init__(self, loops):
        self.wins = 0
        self.loops = loops
        self.turns_won_in = []

    def submit(self, finished_game):
        if finished_game.state == "win":
            self.wins += 1
            self.turns_won_in.append(game.turn_no)
      
    def get_stats(self):
        data = {}
        win_rate = (self.wins / self.loops) * 100
        data["win_rate"] = win_rate
        data["avg_turns"] = sum(self.turns_won_in) / len(self.turns_won_in)
        return data
        


loops = 7

tracker = SolveTracker(loops=loops)

i = 0
while i < loops:
    game = Wordle()
    game.turn("hello")
    while game.state == "active":
        guess = random.choice(game.get_remaining_words)
        game.turn(guess)
    i += 1
    tracker.submit(game)

print(tracker.get_stats())