# PyWordle

PyWordle is a **simple** framework written in Python that helps you build your own Wordle solving algorithms!

<br>

### Table of Contents

- [What is it?](#what-is-it)
- [Installation](#installation)
- [How does it work?](#how-does-it-work)
- [Creating an example solver](#creating-an-example-solver)
  1. [Create the file/folder structure](#s1)
  2. [Import wordlists](#s2)
  3. [Copy the solver template to run.py](#s3)
  4. [Create the solving algorithm in solver.py](#s4)
  5. [Import the solver into run.py](#s5)
  6. [Run the solver!](#s6)
- [Learning the framework](#learning-the-framework)
  - [Create an instance of a game](#create-an-instance-of-a-game)
  - [Playing a turn](#playing-a-turn)
  - [The Wordle class](#the-wordle-class)
- [Included examples](#included-examples)
  - [CLI Game (visual debugger)](#cli-game)
  - [Unknown word solver](#unknown-word-solver)
  - [My solver (maximise_similarity)](#my-solver)

<br>

## <a name="what-is-it">What is it?</a>

PyWordle let's you simulate and automate Wordle games to run against solving algorithms. It provides a simple template (`solver_template.py` found under `pywordle/examples/solver_template`) which lets you 'plug and play' solvers. PyWordle offers several key sets of data to help create solvers, such as the `get_remaining_answers` property which eliminates answers from a designated `valid_answer_list` and returns a list of the possible remaining answers. 



## <a name="installation">Installation</a>

Clone this project, create a new virtual environment at the root of the project, and install it as a Python package in 'editable' mode.

```bash
~/pywordle$  clone https://github.com/nestcx/pywordle.git
~/pywordle$  venv .venv && . .venv/bin/activate
(.venv) ~/pywordle$  pip install -e
```



### <a name="how-does-it-work">How does it work?</a>

Under `pywordle/examples/solver_template` you can find the basic solver template called `solver_template.py` which runs a simple algorithm against an entire answer list.

```Python
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
        game = Wordle(gametype='index', word_index=i)

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
```



```bash
(.venv) ~/pywordle$ python examples/solver_template/solver_template.py 
```

![solver_running](https://i.imgur.com/aIivtH3.gif) 





You can set up games that run under specific circumstances while it keeps track of keyboard data, game states, turn history, as well as data structures that maintain letter matches and letter frequencies and more. 

When running multiple games at a time you can submit each game instance to a `SolveTracker` which will keep track of overall `wins`, `losses`, `loss_answers`, and `turn_history`, and can output a graph that displays the amount of games that were completed in x amount of turns.





### <a name="creating-an-example-solver">Creating an example solver</a>

This solver will select words at random from the answers list.



#### <a name="s1">1)  Create the folder/file structure</a>

```
pywordle/solver1/run.py
pywordle/solver1/solver.py
```



#### <a name="s2">2)  Import wordlists</a>

Wordlists are stored as text files in `pywordle/data`. Included are three wordlists, and you can add more.

After that the data must be through the `pywordle/__init__.py` file in the following format:

```Python
MY_WORD_LIST = files(pywordle.data).joinpath('my_word_list.txt')
```

This is then imported in `run.py` and used when creating a game instance, for example:

```python
from pywordle import MY_WORD_LIST
game = Wordle(valid_guess_list = MY_WORD_LIST, valid_answer_list = VALID_ANSWER_LIST)
```



#### <a name="s3">3) Copy the solver template into run.py</a>

The solver template can be found at `pywordle/examples/solver_template/solver_template.py`.



#### <a name="s4">4) Create the solving algorithm in solver.py</a>

```Python
def _alg(answers)
	return random.choice(answers)

def determine_best_guess(game):
	return _alg(game.get_remaining_answers)
```



#### <a name="s5">5) Import the solver into run.py</a>

`determine_best_guess()` is our entry point into the algorithm, and should be set up to return the next guess for the game loop in `run.py` to use, as is set up already in the template.

```Python
from pywordle.solver1.solver import determine_best_guess
```



#### <a name="s1">6) Run the solver!</a>

```bash
(.venv) ~/pywordle$ python solver1/run.py
```



### <a name="learning-the-framework">Learning the framework</a>



#### <a name="create-an-instance-of-a-game">**Create an instance of a game**</a>

There are four different gametypes available based on where the `answer` comes from. The gametypes are:

- `random` 
  - selects a random `answer` from the `valid_answer_list`.
  - `game = Wordle(gametype = 'random')`
- `unknown` 
  - the game has no knowledge of the `answer`.
  - `game = Wordle(gametype = 'unknown')`
- `select`
  - provide a specific answer.
  - `game = Wordle(gametype='select', answer = 'leaps')`
-  `index`
  - selects the `answer` from the `valid_answer_list` at a certain index.
  - `game = Wordle(gametype='index', answer_index=55)`



The game instance also takes the following optional arguments:

`turn_limit`, default `6`

`valid_guess_list`, default `DEFAULT_GUESS_LIST`

`valid_answer_list`, default `DEFAULT_ANSWER_LIST`

`gamestate`, default `None`



#### <a name="playing-a-turn">Playing a turn</a>

Playing a turn involves providing a guess to the `turn` method, or a `colour_sequence` if the `gametype` is set to `unknown`. This is for when you are playing an external game, you input the colours it returns.

For example, if the response from a turn was

![turn_response](https://i.imgur.com/IfL6x7R.png) 

You would pass `[1, 0, 2, 0, 0]`, where 1 corresponds to green, 2 to yellow, and 0 to black.

```Python
game = Wordle(gametype='select', answer='leaps')
game.turn('hello')
```

```Python
game = Wordle(gametype='unknown')
game.turn('hello', [1, 0, 2, 0, 0])
```

See the `solve_unknown_word` example under `pywordle/examples`.



`Wordle.turn` will return a colour sequence indicating the games response from the turn, in the form of a list [0,1,2,2,0]



#### <a name="the-wordle-class">**The Wordle class**</a>

Please see internal documentation at `pywordle/pywordle/pywordle.py` for information on the class attributes, properties, and methods operate.





### <a name="included-examples">Included examples</a>



#### <a name="cli-game">CLI Game (Debugging interface)</a>

location: `pywordle/examples/cli_game`

![cli_game](https://i.imgur.com/cMMAKSX.gif) 



#### <a name="solve-unknown-word">Unknown word solver</a>

location: `pywordle/examples/solve_unknown_word`

This is used for solving games that are running externally. 

![unknown_word_solver](https://i.imgur.com/Kxmwomg.gif)



#### <a name="solve-unknown-word">My solver (maximise_similarity)</a>

location: `pywordle/examples/maximise_similarity` 

This solver has a 100% success rate with an average of 3.65 guesses.

