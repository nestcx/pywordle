import pywordle.data
from importlib_resources import files

DEFAULT_ANSWER_LIST = files(pywordle.data).joinpath('allowed_answers.txt')
DEFAULT_GUESS_LIST = files(pywordle.data).joinpath('allowed_guesses.txt')
MY_WORD_LIST = files(pywordle.data).joinpath('wordlist.txt')