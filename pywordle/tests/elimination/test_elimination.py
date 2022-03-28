from pywordle.pywordle.pywordle import Wordle
import json


def test_edges():
    game = Wordle(gametype="select", answer="edges")
    f = open('tests/elimination/edges.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_answers == guesses[g]


def test_spays():
    game = Wordle(gametype="select", answer="spays")
    f = open('tests/elimination/spays.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_answers == guesses[g]


def test_condo():
    game = Wordle(gametype="select", answer="condo")
    f = open('tests/elimination/condo.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_answers == guesses[g]


def test_lying():
    game = Wordle(gametype="select", answer="lying")
    f = open('tests/elimination/lying.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_answers == guesses[g]


def test_crime():
    game = Wordle(gametype="select", answer="crime")
    f = open('tests/elimination/crime.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_answers == guesses[g]


def test_myrrh():
    game = Wordle(gametype="select", answer="myrrh")
    f = open('tests/elimination/myrrh.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_answers == guesses[g]


def test_tenth():
    game = Wordle(gametype="select", answer="tenth")
    f = open('tests/elimination/tenth.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_answers == guesses[g]


def test_aloof():
    game = Wordle(gametype="select", answer="aloof")
    f = open('tests/elimination/aloof.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_answers == guesses[g]


def test_chief():
    game = Wordle(gametype="select", answer="chief")
    f = open('tests/elimination/chief.json', 'r')

    guesses = json.load(f)

    for g in guesses:
        game.turn(g)
        assert game.get_remaining_answers == guesses[g]
        