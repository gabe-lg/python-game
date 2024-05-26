from Game import *
from obj.UserInput import *

if __name__ == "__main__":
    user_input = UserInput()
    user_input.modify()

    event: Event = Event()
    game: Game = Game(event)
    game.init(user_input)
    game.start()
    event.start()
