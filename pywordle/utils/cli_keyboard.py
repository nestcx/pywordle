from pywordle.utils.cli_colour_string import *

rows = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
['a', 's', 'd', 'f','g', 'h', 'j', 'k', 'l'],
['z', 'x', 'c', 'v', 'b', 'n', 'm']]

def __generate_coloured_row(row, keyboard):
    out = ""
    for r in row:
        if r in keyboard["green"]:
            out += colour_string(GREEN, BLACK, r)
        elif r in keyboard["yellow"]:
            out += colour_string(YELLOW, BLACK, r)
        elif r in keyboard["black"]:
            out += colour_string(BLACK, LIGHTGREY, r)
        else:
            out += colour_string(LIGHTGREY, BLACK, r)
    return out

def generate_coloured_keyboard(keyboard):
    out = ""
    out += __generate_coloured_row(rows[0], keyboard) + '\n'
    out += " " + __generate_coloured_row(rows[1], keyboard) + '\n'
    out += "   " + __generate_coloured_row(rows[2], keyboard) + '\n'

    return out