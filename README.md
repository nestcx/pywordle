# Pywordle

PyWordle is a simple framework written in Python that helps you build your own Wordle solving algorithms!

<br>

### Table of Contents

- [What is it?](#what-is-it)
- [Installation](#installation)
- [How does it work?](#how-does-it-work)
- [Learning the framework](#learning-the-framework)
  - [Create an instance of a game](#create-an-instance-of-a-game)
  - [Playing a turn](#playing-a-turn)
  - [The properties](#the-properties)
- [Creating an example solver](#creating-an-example-solver)
  1. [Create the file/folder structure](#s1)
  2. [Import wordlists](#s2)
  3. [Copy the solver template to run.py](#s3)
  4. [Create the solving algorithm in solver.py](#s4)
  5. [Import the solver into run.py](#s5)
  6. [Run the solver!](#s6)
- [Included examples](#included-examples)
  - [CLI Game (visual debugger)](#cli-game)
  - [Unknown word solver](#unknown-word-solver)
  - [My solver (maximise_similarity)](#my-solver)

<br>

## <a name="what-is-it">What is it?</a>

PyWordle let's you simulate and automate Wordle games to run against solving algorithms. It provides a simple template (`solver_template.py` found under `pywordle/examples/solver_template`) which lets you 'plug and play' solvers. 

PyWordle offers several key sets of data to help create solvers, such as the `get_remaining_answers` property which eliminates answers from a designated `valid_answer_list` and returns a list of the possible remaining answers. 



<br>

## <a name="installation">Installation</a>

Clone this project, create a new virtual environment at the root of the project, and install it as a Python package in 'editable' mode.

```bash
~/pywordle$  clone https://github.com/nestcx/pywordle.git
~/pywordle$  venv .venv && . .venv/bin/activate
(.venv) ~/pywordle$  pip install -e
```

<br>

## <a name="how-does-it-work">How does it work?</a>

You supply an algorithm which determines the next best guess for a game instance, and PyWordle handles the rest.

It can be as simple as:

```python
def determine_best_guess(game):
	return random.choice(game.get_remaining_answers)

game = Wordle()

while game.state == "active":
    guess = determine_best_guess(game)
    game.turn(guess)
    
    if game.state == "win":
                print("yay!")
```

<br>

In `pywordle/examples/solver_template` you can find the basic solver template `solver_template.py` which runs a simple algorithm against an entire answer list.

```bash
(.venv) ~/pywordle$ python examples/solver_template/solver_template.py 
```

![solver_running](https://i.imgur.com/aIivtH3.gif) 

<br>


You can set up games that run under specific circumstances while it keeps track of keyboard data, game states, turn history, as well as data structures that maintain letter matches and letter frequencies and more. 

<br>

When running multiple games at a time you can submit each game instance to a `SolveTracker` which will keep track of overall `wins`, `losses`, `loss_answers`, and `turn_history`, and can output a graph that displays the amount of games that were completed in x amount of turns.

<br>



## <a name="learning-the-framework">Learning the framework</a>



### <a name="create-an-instance-of-a-game">**Create an instance of a game**</a>

There are four different gametypes available based on where the `answer` comes from.

```python
# selects a random answer from the valid_answer_list
game = Wordle(gametype = 'random')

# the game has no knowledge of the answer
game = Wordle(gametype = 'unknown')

# provide a specific answer
game = Wordle(gametype='select', answer='leaps')

# select the answer from the valid_answer_list at a certain index
game = Wordle(gametype='index', answer_index=55)
```

<br>

In total, the game instance maintains the following 13 attributes:

```
valid_guess_list : list (default DEFAULT_GUESS_LIST)
valid_answer_list : list (default DEFAULT_ANSWER_LIST)
gametype : str (default 'random')
answer : str (default None)
turn_no : int (default 1)
turn_limit : int (default 6)
state : str (default 'active')

turn_history : dict 
direct_matches : dict
indirect_matches : dict
definitive_frequency : dict
potential_frequency : dict
blacklist : list
```

<br>

The full constructor definition is as follows

```Python
def __init__(self, 
             gamestate = None, 
             gametype = 'random', 
             answer = None, 
             answer_index = None, 
             turn_limit = 6, valid_guess_list = DEFAULT_GUESS_LIST, 
             valid_answer_list = DEFAULT_ANSWER_LIST)
```

<br>

Examples

```python
# create game with default arguments
game = Wordle()

# set the guess and answer lists
game = Wordle(valid_guess_list=MY_LIST, valid_answer_list=MY_LIST)

# create a 'random' game with the default word lists, with a turn limit of 10
game = Wordle(turn_limit=10)

# create a default game, and copy it's state to initialize another game instance
game1 = Wordle()
game2 = Wordle(gamestate=game1.gamestate)
```

<br>

### <a name="playing-a-turn">Playing a turn</a>

```Python
game = Wordle(gametype='select', answer='leaps')
game.turn('hello')
```



`Wordle.turn` returns a colour sequence in the form of a list:

```python
[1,0,2,0,0]

# 1 = GREEN
# 2 = YELLOW
# 3 = BLACK
```

This list would represent the turn below:

<img src="https://i.imgur.com/IfL6x7R.png" alt="turn_response" style="zoom:67%;" /> 

<br>

When the `gametype` is set to `unknown`, a `guess` AND a `colour_sequence` must be provided. If the word is not known to the game then it cannot generate the colour sequence it self.

```Python
game = Wordle(gametype='unknown')
game.turn('hello', [1, 0, 2, 0, 0])
```

(See the `solve_unknown_word` example under `pywordle/examples`)

<br>

Behind the scenes, `Wordle.turn` does the following:

- validates the guess against the `valid_guess_list`

- processes the guess in `process_guess()`

  - updates the following four data structures (used primarily for the property `get_remaining_answers`:

    - `direct_matches`
    - `indirect_matches`
    - `potential_frequency`
    - `definitive_frequency`
    - `blacklist`

  - generates a colour sequence

- records the turn in `turn_history`

- increases the `turn_no` by 1

- returns the colour sequence

<br>

### <a name="the-properties">The properties</a>


```
get_remaining_answers : list
    returns a list of possible remaining answers.
    example: ['apple', 'ample', 'achey']

get_keyboard_data : dict
    returns state of letter colours, used to create coloured keyboards
    for visual feedback.
    example: {'green': {'a', 'l'}, 'yellow': {'k'}, 'black': ['h', 'e']}
        
get_keystrokes : list
    returns a list of every letter that has guessed.
    example: ['a', 'e', 'w']

gamestate : dict
    the 'gamestate' is defined by the state of the instance attributes.
    these attributes are copied and returned in a dictionary.

true_yellow : dict
    returns a dict of letters that are considered 'true yellow'.
    a 'true yellow' letter is a letter that has been 'yellowed' and has
    not been found (turned green) yet.
    example: {'e': [1], 'i': [1]}
```

<br>

Please see internal documentation at `pywordle/pywordle/pywordle.py` for information on the class attributes, properties, and methods operate.

<br>



## <a name="creating-an-example-solver">Creating an example solver</a>

This solver will select words at random from the answers list.



### <a name="s1">1)  Create the folder/file structure</a>

```
pywordle/solver1/run.py
pywordle/solver1/solver.py
```

<br>

### <a name="s2">2)  Import wordlists</a>

Wordlists are stored as text files in `pywordle/data`. Three are included, and you can add more.

The wordlists must be added to `pywordle/__init__.py` file in the following format:

```Python
MY_WORD_LIST = files(pywordle.data).joinpath('my_word_list.txt')
```

They can then be imported in `run.py` and used when creating a game instance, for example:

```python
from pywordle import MY_WORD_LIST
game = Wordle(valid_guess_list = MY_WORD_LIST, valid_answer_list = VALID_ANSWER_LIST)
```

<br>

### <a name="s3">3)  Copy the solver template into run.py</a>

The full solver template can be found at `pywordle/examples/solver_template/solver_template.py`.

```python
# import Wordle class
from pywordle.pywordle.pywordle import Wordle

# import SolveTracker class
from pywordle.utils.solvetracker import SolveTracker


# determine how many times to loop
game_count = len(Wordle().valid_answer_list)

tracker = SolveTracker(turn_limit=6)


with alive_bar(game_count) as bar:
    for i in range(0, game_count):
		
        # the gametype 'index' sets the answer to the nth answer in the answers list
        game = Wordle(gametype='index', word_index=i)

        while game.state == "active":
            # we need to integrate our solver here!
            guess = ...
            game.turn(guess)

            if game.state == "loss":
                print(game.answer)

        tracker.submit(game)
        clear_terminal()
        print(tracker.get_graph())
        
        bar()

print(tracker.get_stats())
```



<br>

### <a name="s4">4)  Create the solving algorithm in solver.py</a>

```Python
def _alg(answers)
	return random.choice(answers)

def determine_best_guess(game):
	return _alg(game.get_remaining_answers)
```

<br>

### <a name="s5">5)  Import and integrate the solver into run.py</a>

`determine_best_guess()` is our entry point into the algorithm, and should be set up to return the next guess for the game loop in `run.py` to use, as is set up already in the template.

```Python
from pywordle.solver1.solver import determine_best_guess

...
			while game.state == "active":
        
                # the solver returns it's best 'guess' to play.
                guess = determine_best_guess(game)
                game.turn(guess)
...
```



<br>

### <a name="s1">6)  Run the solver!</a>

```bash
(.venv) ~/pywordle$ python solver1/run.py
```

<br>



## <a name="included-examples">Included examples</a>



### <a name="cli-game">CLI Game (Debugging interface)</a>

location: `pywordle/examples/cli_game`

![cli_game](https://i.imgur.com/cMMAKSX.gif) 

<br>

### <a name="solve-unknown-word">Unknown word solver</a>

location: `pywordle/examples/solve_unknown_word`

This is used for solving games that are running externally. 

![unknown_word_solver](https://i.imgur.com/Kxmwomg.gif)

<br>

### <a name="solve-unknown-word">My solver (maximise_similarity)</a>

location: `pywordle/examples/maximise_similarity` 

This solver has a 100% success rate with an average of 3.65 guesses.

<br>
<br>
<hr>
<br>

Created by Marcus LV (2022)

