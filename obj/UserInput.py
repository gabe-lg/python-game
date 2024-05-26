from const import *


class UserInput(object):
    """
    Keeps track of user input regarding the desired window width and height,
    and refresh rate of the game
    Inherits `width`, `height` and `dt` from App
    """
    def __init__(self):
        """
        Initializes attributes with their default values
        """
        self.width = 1280
        self.height = 720
        self.dt = 60

    def modify(self):
        """
        Prompts user input and changes values of `width`, `height` and `dt`
        If no input received, leaves values unchanged
        """
        try:
            inputs = INPUTS

            for i in range(len(inputs)):
                inp = input(inputs[i][0])
                if inp:
                    inputs[i][1] = int(inp)
                    assert inputs[i][1] > 0

            self.width = inputs[0][1]
            self.height = inputs[1][1]
            self.dt = inputs[2][1]

            self.assert_inv()

            print(f"Success! Launching game with width = {self.width}, "
                  f"height = {self.height}, and refresh rate = {self.dt}.")
        except (ValueError, AssertionError):
            print("Please enter a positive integer.")
            self.modify()

    def assert_inv(self):
        """
        Asserts class invariants
        """
        assert isinstance(self.width, int)
        assert isinstance(self.height, int)
        assert isinstance(self.dt, int)
        assert self.width > 0 and self.height > 0 and self.dt > 0
