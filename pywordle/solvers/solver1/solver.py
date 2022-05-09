import random

def _alg(answers):
	return random.choice(answers)

def determine_best_guess(game):
	return _alg(game.get_remaining_answers)