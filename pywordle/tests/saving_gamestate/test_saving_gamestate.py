from pywordle.pywordle.pywordle import Wordle

def test_gamestate_dict():
    game = Wordle(answer="marks", gametype="select")
    game.turn("wings")
    game.turn("spend")
    gamestate = game.gamestate

    assert gamestate["turn_no"] == 3
    assert gamestate["gametype"] == "select"
    assert gamestate["definitive_frequency"] == {"s": 1}


def test_gamestate_loads():
    game = Wordle(answer="marks", gametype="select")
    game.turn("wings")
    game.turn("spend")
    gamestate = game.gamestate

    game2 = Wordle(gamestate=gamestate)
    gamestate2 = game2.gamestate
    assert gamestate2["turn_no"] == 3
    assert gamestate2["gametype"] == "select"
    assert gamestate2["definitive_frequency"] == {"s": 1}









