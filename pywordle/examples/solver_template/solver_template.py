import random
from alive_progress import alive_bar
from pywordle.utils import clear_terminal

# import Wordle class
from pywordle.pywordle.pywordle import Wordle

# import SolveTracker class
from pywordle.utils.solvetracker import SolveTracker



# our wonderful algorithm
def determine_best_guess(game):
    return random.choice(game.get_remaining_answers)


# determine how many times to loop
game_count = len(Wordle().valid_answer_list)

tracker = SolveTracker(turn_limit=6)

with alive_bar(game_count) as bar:
    for i in range(0, game_count):
		
        # the gametype 'index' sets the answer to the nth answer in the answers list
        game = Wordle(gametype='index', answer_index=i)

        while game.state == "active":
            # the solver returns the it's best 'guess' to play.
            guess = determine_best_guess(game)
            game.turn(guess)

            if game.state == "loss":
                print(game.answer)

        tracker.submit(game)
        clear_terminal()
        print(tracker.get_graph())
        
        bar()

print(tracker.get_stats())