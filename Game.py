from const import *
from obj import *


class Game(Thread):
    """
    Initializes pygame and updates the screen
    """

    # Hidden attributes:
    # :ivar Event event: Event object keeping track of key presses
    # :ivar int _width: width of window; width > 0
    # :ivar int _height: height of window; height > 0
    # :ivar int _dt: FPS of the game; dt > 0
    # :ivar pygame.surface.Surface _screen: screen displaying the game
    # :ivar pygame.time.Clock _clock: pygame clock keeping track of the refresh rate
    # :ivar bool _running: True if game is running; False otherwise

    # Game attributes:
    # :ivar int _state: keeps track of the state of the game
    # :ivar bool _paused: whether the game is paused by user
    # :ivar int _score: player's score; score >= 0
    # :ivar Player _player: player's avatar
    # :ivar list[Text | Empty] _text: list of Text objects
    # :ivar list[Floor | Empty] _floor: list of Floor objects keeping player from falling
    # :ivar list[Powerup | Empty] _powerup: list of Powerup objects
    # :ivar Settings | Empty _settings: settings button

    def __init__(self, event):
        """
        Initializes an App object with default values
        :param Event event: Event object keeping track of key presses
        """
        super().__init__()

        # An empty object
        empty:          Empty = Empty()

        # Hidden attributes
        self._event:    Event = event
        self._width:    int = 1280
        self._height:   int = 720
        self._dt:       int = 60
        self._screen:   pygame.surface.Surface
        self._clock:    pygame.time.Clock
        self._running:  bool = False

        # Game attributes
        self._state:    int = INIT
        self._paused:   bool = False
        self._score:    int = 0
        self._player:   Player = None
        self._text:     list[Text | Empty] = [empty for _ in range(2)]
        self._floor:    list[Floor | Empty] = [empty]
        self._powerup:  list[Powerup | Empty] = [empty]
        self._settings: Settings | Empty = Settings()

    @property
    def event(self) -> Event:
        """
        :return: Event object keeping track of key presses
        """
        return self._event

    @event.setter
    def event(self, event) -> None:
        """
        :param Event event: Event object keeping track of key presses
        """
        self._event = event

    def init(self, user_input) -> None:
        """
        Initializes an App object based on the attributes of an UserInput object
        :param UserInput user_input: UserInput object with attributes storing user input
        """
        pygame.init()

        # rewrite attributes according to user input
        self._width = user_input.width
        self._height = user_input.height
        self._dt = user_input.dt

        self._screen = pygame.display.set_mode((self._width, self._height))
        self._clock = pygame.time.Clock()
        self._running = True

    def update(self) -> None:
        """
        Animates a single frame in the game, and draws it on the screen
        """
        self._screen.fill("white")  # clears last frame

        # animate frame
        self._states()
        self._assert_inv()

        self._event.delete_key()  # deletes last keypress

        # draw objects
        for i in self._text:
            i.draw(self._screen)
        for i in self._floor:
            i.draw(self._screen)
        for i in self._powerup:
            i.draw(self._screen)
        self._settings.draw(self._screen)

        pygame.display.update()  # updates screen
        self._clock.tick(self._dt)  # wait until next update

    def run(self) -> None:
        """
        Calls update method while the game is running
        """
        while self._running:
            self.update()
        self.event.running = False
        pygame.quit()

    # == private methods == #
    def _assert_inv(self) -> None:
        """
        Asserts class invariants
        """
        assert -1 <= self._state < 5  # TODO

    def _key_pressed(self, key) -> bool:
        """
        Checks if a key was pressed
        :param int key: the key meant to be checked
        :return: True if key was the last key pressed; False otherwise
        """
        keys: list[int] = self.event.get_key
        return keys != [] and keys[-1] == key

    @staticmethod
    def _key_held(key) -> bool:
        """
        Checks if a key was held down
        :param int key: the key meant to be checked
        :return: True if key is being held down; False otherwise
        """
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        return keys[key]

    def _mouse_over_settings(self) -> None:
        """
        Detects the mouse over settings and show/hide text accordingly. Always
        runs regardless of game state. Moreover, if settings icon is pressed
        while the mouse is over it, initializes settings screen.
        """
        settings_text: Text | Empty
        if self._settings.mouse_over():
            # mouse over settings icon: display text
            settings_text = Text("Settings", "RetroGame", 20,
                                 xpos=-1.0, ypos=self._settings.ypos,
                                 pos_x=self._settings.xpos - 5.0)
            # left click on settings icon
            # (3 for three buttons of the mouse; [0] to retrieve the left button)
            if pygame.mouse.get_pressed(3)[0]:
                # initialize settings screen
                self._settings_init()
        else:
            # delete text
            settings_text = Empty()
        self._text[TEXT_SETTINGS] = settings_text

    def _settings_init(self) -> None:
        """
        Initializes the settings screen when the settings icon is pressed.
        """
        empty: Empty = Empty()
        self._settings = empty
        self._text = [empty for _ in range(20)]
        self._paused = True

        # == create objects == #
        # title
        title: Text = Text("Settings", "Arcade", 100, screen=self._screen)
        self._text[TEXT_TITLE] = title
        title.ypos = 20.0

    def _settings_main(self) -> None:
        """
        Displays the settings screen when state is `SETTINGS`
        """
        # menu
        # TODO

        # # == animations == #
        # if 14.0 <= title.ypos:
        #     title.ypos += 2.0
        # elif title.ypos >= 26.0:
        #     title.ypos -= 2.0
        # else:
        #     title.ypos += random() * 16 - 8

        # == close == #
        if self._key_pressed(pygame.K_x):
            self._paused = False
            self._settings = Settings()
            self._settings.place(self._screen)
            self._text = [Empty() for _ in range(2)] # FIXME should restore to prev text

    # == states == #
    def _states(self) -> None:
        """
        Determines game behavior depending on the state of the game.
        Main game thread
        """
        # used in `move` methods
        arrows: tuple[bool, bool, bool, bool] = (
            self._key_held(pygame.K_w), self._key_held(pygame.K_a),
            self._key_held(pygame.K_s), self._key_held(pygame.K_d))

        # if esc pressed, quit game immediately
        if self._key_pressed(pygame.K_ESCAPE):
            self._running = False
            return

        # react to whether the mouse is over the settings icon
        self._mouse_over_settings()

        # if game is paused, run `self._settings_main()` and return immediately
        if self._paused:
            self._settings_main()
            return

        # == states == #
        if self._state == INIT:
            self._state_init()

        if self._state == START_SCREEN:
            self._state_start_screen()

        if self._state == NEW_GAME:
            self._state_new_game(arrows)

        if self._state == GAME_RUNNING:
            self._state_game_running(arrows)

    def _state_init(self) -> None:
        """
        Creates objects for start screen, run once when app starts and state
        is `INIT`. Changes state to `START_SCREEN`
        """
        self._text[TEXT_WELCOME] = Text("Welcome!", "Arcade", 100,
                                        screen=self._screen)
        self._settings.place(self._screen)

        # change state
        self._state = START_SCREEN

    def _state_start_screen(self) -> None:
        """
        Controls the start screen when state is `START_SCREEN`
        """
        #print(pygame.mouse.get_pos(), (self._settings.xpos, self._settings.ypos), self._settings.center())
        if self._key_held(pygame.K_a):
            print("before:", (self._settings.xpos, self._settings.ypos), self._settings.center())
            self._settings.rotozoom(5.0, 2.0)
            print("after:", (self._settings.xpos, self._settings.ypos), self._settings.center())
            print()

        # space pressed: start new game
        if self._key_pressed(pygame.K_SPACE):
            self._state = NEW_GAME

    def _state_new_game(self, arrows) -> None:
        """
        Controls the game when state is `NEW_GAME`. Run once and changes game
        state to `GAME_RUNNING`
        :param tuple[bool, bool, bool, bool] arrows: see method `move` of
            `GameObject`
        """
        self._screen.fill("blue")

        # change state
        self._state = GAME_RUNNING
        raise NotImplementedError()  # TODO

    def _state_game_running(self, arrows) -> None:
        """
        TODO write spec
        """
        raise NotImplementedError()  # TODO
