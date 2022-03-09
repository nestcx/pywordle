GREEN = "40"
YELLOW = "226"
BLACK = "16"
LIGHTGREY = "7"
DARKGREY = "238"
WHITE = "255"

def colour_string(background, foreground, letter):
    return f"\033[1;48;5;{background};38;5;{foreground}m {letter} \033[0m"