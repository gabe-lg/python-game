# == MAIN VARIABLES == #
# lists of prompts for user input
INPUTS = [["Please enter width of game window (default 1280px): ", 1280],
          ["Please enter height of game window (default 720px): ", 720],
          ["Please enter the refresh rate of the game (default 60 FPS): ", 60]]

# == APP VARIABLES == #
# states
SETTINGS:       int = -1
INIT:           int = 0
START_SCREEN:   int = 1
NEW_GAME:       int = 2
GAME_RUNNING:   int = 3

# == GAMEOBJECT VARIABLES == #
# == text == #
TEXT_SETTINGS:  int = 0

# == start screen == #
TEXT_WELCOME:   int = 1

# == settings == #
TEXT_TITLE:     int = 10
