from obj.GameObject import *


class Text(GameObject):
    """
    Object that displays text on screen
    """

    def __init__(self, text, font, size, color=(0, 0, 0),
                 xpos=None, ypos=None, screen=None, pos_x=None, is_test=False):
        """
        Attribute `image` is the text rectangle
        :param str text: text to put on the screen
        :param str font: path to font file
        :param int size: size of text; size > 0
        :param tuple[int, int, int] color: color of the text as RGB values;
         all `ints` in `color` >= 0.
         default: (0, 0, 0)
        :param float xpos: x position of upper-left corner of object; `xpos` >= 0.
         default: `xpos` = None meaning xpos is not given; in that case, requires
         `ypos` is None
         * special case: if x == -1.0, run place_left; in that case, requires
         `pos_x` is not None
        :param float ypos: y position of upper-left corner of object; `ypos` >= 0.
         default: `ypos` = None meaning ypos is not given; in that case, requires
         `xpos` is None
        :param pygame.surface.Surface screen: main screen of the game
         default: `screen` = None; in that case, requires `xpos` is not None
        :param float pos_x: the desired position of the object's right border
         default: `pos_x` = None; in that case, requires `xpos` != -1.0
        :param bool is_test: whether the object is used for a test; default `False`
        """
        # `font`: if no extension given, append it
        if len(font) < 4 or ("." not in font and font[-4: -1] != ".ttf"):
            font += ".ttf"
        path: str = "../" * is_test + "fonts/" + font

        # text
        assert isinstance(text, str)
        # font
        assert isinstance(font, str) and exists(path)
        # size
        assert isinstance(size, int) and size > 0
        # color
        for i in color:
            assert isinstance(i, int) and i >= 0
        # xpos / ypos / screen
        assert ((xpos is None and ypos is None and screen is not None) or
                (xpos is not None and ypos is not None))
        # xpos / pos_x
        if xpos == -1.0:
            assert pos_x is not None

        if xpos is None:
            super().__init__(0.0, 0.0, is_test=is_test)
        elif xpos == -1.0 and ypos != -1.0:
            super().__init__(0.0, ypos, is_test=is_test)
        else:
            # ivar image will be overwritten
            super().__init__(xpos, ypos, is_test=is_test)

        self._font: pygame.font.Font = pygame.font.Font(path, size)

        # overwrite img
        self.image_orig = self._font.render(text, True, color)
        self.image = self.image_orig

        # `place` if no xpos or ypos given
        if xpos is None:
            self.place(screen)
        # `place
        elif xpos == -1.0 and ypos != -1.0:
            self.place_left(pos_x)

    def place(self, screen) -> None:
        assert isinstance(screen, pygame.surface.Surface)

        # center of the screen
        w: float = self.image_orig.get_width()
        h: float = self.image_orig.get_height()
        self.xpos = (screen.get_width() - w) / 2
        self.ypos = (screen.get_height() - h) / 2
