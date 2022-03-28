from pywordle.utils.clear_terminal import clear_terminal
from pywordle.pywordle.pywordle import Wordle
from pywordle.utils.solvetracker import SolveTracker
from alive_progress import alive_bar
from maximise_similarity import determine_best_guess

game_count = len(Wordle().valid_answer_list)
tracker = SolveTracker(turn_limit=6)

with alive_bar(game_count, stats=False) as bar:
    for i in range(0, game_count):

        game = Wordle(gametype="index", answer_index=i)
        game.turn('salet')

        while game.state == "active":
            
            remaining_words = game.get_remaining_answers

            guess = determine_best_guess(game)
            
            turn = game.turn(guess)

            if game.state == "loss":
                print(game.answer)

        tracker.submit(game)
        clear_terminal()
        print(tracker.get_graph())
        bar()

print()
print(f'win rate: {tracker.get_stats()["win_rate"]}')
print(f'average turns: {tracker.get_stats()["avg_turns"]}')
print(tracker.get_graph())
