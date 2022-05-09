from pywordle.utils.clear_terminal import clear_terminal
from pywordle.pywordle.pywordle import Wordle
from pywordle.utils.solvetracker import SolveTracker
from alive_progress import alive_bar
from maximise_similarity import determine_best_guess
import json

offset = 0
game_count = len(Wordle().valid_answer_list)
tracker = SolveTracker(turn_limit=6)

with alive_bar(game_count, stats=False) as bar:
    for i in range(offset, game_count):

        game = Wordle(gametype="index", answer_index=i)
        game.turn('slate')

        while game.state == "active":
            
            guess_response = determine_best_guess(game)

            turn = game.turn(guess_response)

        tracker.submit(game)
        clear_terminal()
        print(tracker.get_graph())
        bar()

print()

stats = tracker.get_stats()

print(f'win rate: {stats["win_rate"]}')
print(f'average turns: {stats["avg_turns"]}')
print(f'average turns: {stats["total_turns"]}')
print(f'loss answers: {stats["loss_answers"]}')

print(tracker.get_graph())


#f = open("dump.json", "w")
#f.write(json.dumps(tracker.turn_history))
#f.close()