from obj.GameObject import *


class Settings(GameObject):
    """
    The settings button
    """
    @property
    def open(self) -> bool:
        """
        :return:
        """
        return self._open

    @open.setter
    def open(self, open) -> None:
        """
        :param bool open:
        """
        self._open = open

    def __init__(self):
        super().__init__(0.0, 0.0, "settings.svg")
        self.open = False

    def place(self, screen) -> None:
        w_screen: int = screen.get_width()
        width: float = 24.0
        scale: float = w_screen / width
        self.resize(2.0)

        # NE corner of the screen
        self.xpos = w_screen - self.image.get_width()
        self.ypos = 0.0

        # w: float = self.image_orig.get_width()
        # h: float = self.image_orig.get_height()
        # self.xpos = (screen.get_width() - w) / 2
        # self.ypos = (screen.get_height() - h) / 2
