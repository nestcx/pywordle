import pywordle.data
from importlib_resources import files

DEFAULT_WORDLIST = files(pywordle.data).joinpath('wordlist.txt')