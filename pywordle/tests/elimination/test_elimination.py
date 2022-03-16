from pywordle.pywordle.pywordle import Wordle
import json

def test_edges():
    game = Wordle(word="edges")
    f = open('tests/elimination/edges.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_words == guesses[g]

def test_spays():
    game = Wordle(word="spays")
    f = open('tests/elimination/spays.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_words == guesses[g]

def test_condo():
    game = Wordle(word="condo")
    f = open('tests/elimination/condo.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_words == guesses[g]

def test_lying():
    game = Wordle(word="lying")
    f = open('tests/elimination/lying.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_words == guesses[g]

def test_crime():
    game = Wordle(word="crime")
    f = open('tests/elimination/crime.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_words == guesses[g]

def test_myrrh():
    game = Wordle(word="myrrh")
    f = open('tests/elimination/myrrh.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_words == guesses[g]

def test_tenth():
    game = Wordle(word="tenth")
    f = open('tests/elimination/tenth.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_words == guesses[g]

def test_aloof():
    game = Wordle(word="aloof")
    f = open('tests/elimination/aloof.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_words == guesses[g]

def test_chief():
    game = Wordle(word="chief")
    f = open('tests/elimination/chief.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_words == guesses[g]
        