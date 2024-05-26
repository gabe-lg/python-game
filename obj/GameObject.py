import math
import pygame
from os.path import exists


class GameObject(object):
    """
    Describes a generic object represented in-game.
    :ivar float xpos: x position of upper-left corner of object; `xpos` >= 0.0
    :ivar float ypos: y position of upper-left corner of object; `ypos` >= 0.0
    :ivar pygame.Surface image_orig: image of object before any rotation
    :ivar pygame.Surface image: image after rotation `angle` degrees counterclockwise
    :ivar float angle: object's angle of rotation counterclockwise in degrees;
        0.0 <= `angle` < 360.0
    :ivar float scale: object's #TODO
    """

    @property
    def xpos(self) -> float:
        """
        :return: xpos
        """
        return self._xpos

    @xpos.setter
    def xpos(self, xpos) -> None:
        """
        :param float xpos:
        """
        self._xpos = xpos

    @property
    def ypos(self) -> float:
        """
        :return: ypos
        """
        return self._ypos

    @ypos.setter
    def ypos(self, ypos) -> None:
        """
        :param float ypos:
        """
        self._ypos = ypos

    @property
    def image(self) -> pygame.Surface:
        """
        :return: image
        """
        return self._image

    @image.setter
    def image(self, image) -> None:
        """
        :param pygame.Surface image:
        """
        self._image = image

    def __init__(self, xpos, ypos, image="foo.png", is_test=False):
        """
        :param float xpos: x position of upper-left corner of object; `xpos` >= 0.0
        :param float ypos: y position of upper-left corner of object; `ypos` >= 0.0
        :param str image: name of image located inside folder `images`. File
         extension mandatory. Default "foo.png" for objects not needing an image
        :param bool is_test: whether the object is used for a test. Default `False`
        """
        path: str = "../" * is_test + "images/" + image

        assert isinstance(xpos, float) and isinstance(ypos, float)
        assert xpos >= 0.0 and ypos >= 0.0
        assert isinstance(image, str) and exists(path)

        self.xpos = xpos
        self.ypos = ypos
        self.image_orig = pygame.image.load(path)
        self.image = self.image_orig

        self._angle = 0.0
        self._scale = 1.0

    def center(self) -> tuple[float, float]:
        """
        :return: tuple containing the x and y coordinates of object's center
        """
        corners = self.get_corners()

        nw: tuple[float, float] = corners[0]
        se: tuple[float, float] = corners[3]

        x: float = (nw[0] + se[0]) / 2
        y: float = (nw[1] + se[1]) / 2

        return x, y

    def collides(self, other) -> bool:
        """
        Determines whether this object overlaps with `other`.
        :param GameObject other: the other object to check for collision
        :return: True if object overlaps with `other`; False otherwise
        """
        assert isinstance(other, GameObject)

        raise NotImplementedError
        # FIXME

    def draw(self, screen) -> None:
        """
        Draws image on the screen and updates `corners` to match the
        current position of object.
        :param pygame.surface.Surface screen: the screen to draw on
        """
        assert isinstance(screen, pygame.surface.Surface)

        center: tuple[float, float] = self.center()
        x_corner: float = center[0] - self.image.get_width() / 2
        y_corner: float = center[1] - self.image.get_height() / 2
        screen.blit(self.image, (x_corner, y_corner))

    def get_corners(self) -> list[tuple[float, float]]:
        """
        Computes the positions of the object's four corners;
        each entry of list contains the x and y positions of the
        NW, NE, SW, and SE corners, in this order.
        :return: four corners as lists of tuples
        """
        corners: list[tuple[float, float]] = []
        w: float = self.image_orig.get_width() * self._scale
        h: float = self.image_orig.get_height() * self._scale
        theta: float = math.radians(self._angle)

        for i in range(4):
            corners.append((self.xpos + w * math.cos(theta) * (i % 2) -
                            h * math.sin(theta) * (i > 1),
                            self.ypos + w * math.sin(theta) * (i % 2) +
                            h * math.cos(theta) * (i > 1)))
        return corners

    def mouse_over(self) -> bool:
        """
        Determines whether the mouse is hovering over the object.
        :return: True if the mouse is hovering over the object; False otherwise
        """

        # mouse coor
        mouse: tuple[int, int] = pygame.mouse.get_pos()
        mouse_x: int = mouse[0]
        mouse_y: int = mouse[1]

        # assume not rotated
        if self._angle == 0:
            return ((self.xpos <= mouse_x <= self.xpos + self.image.get_width()) and
                    (self.ypos <= mouse_y <= self.ypos + self.image.get_height()))
        else:
            raise NotImplementedError

    def move(self, arrows, step) -> None:
        """
        Moves the object `step` px up when W pressed, `step` px to the left when A pressed,
        `step` px down when S pressed, and `step` px to the right when D pressed.
        :param tuple[bool, bool, bool, bool] arrows: entries are True when key
            is pressed; False otherwise; indices 0, 1, 2, 3 represent the keys
            `W`, `A`, `S`, and `D` respectively; `len(arrows)` == 4
        :param float step: number of pixels the object moves when
            one of the keys W, A, S, and D is pressed;
            `step` >= 0
        """
        assert isinstance(arrows, tuple) and len(arrows) == 4
        assert isinstance(step, float) and step >= 0
        for i in arrows:
            assert isinstance(i, bool)

        self.xpos += step * (arrows[3] - arrows[1])
        self.ypos -= step * (arrows[0] - arrows[2])

    def place(self, screen) -> None:
        """
        Resize and place objects in its default position relative to the size
        of the screen. Default implementation does nothing.
        :param pygame.surface.Surface screen: main screen of the game
        """
        pass

    def place_left(self, pos) -> None:
        """
        Modifies the object's `xpos` such that its right border is at `pos`.
        :param float pos: the desired position of the object's right border;
         `pos` >= self.image.get_width()
        """
        assert pos >= self.image.get_width()
        self.xpos = pos - self.image.get_width()

    def resize(self, scale) -> None:
        """
        Resize image by a factor of `scale`; center unchanged.
        :param float scale: the resizing factor; `scale` > 0.0
        """
        assert isinstance(scale, float) and scale > 0.0

        # change scale to satisfy its invar
        self._scale *= scale

        # the change in coor of upper-left corner is half of orig w/h minus new
        self.xpos += self.image.get_width() * (1 - scale) / 2
        self.ypos += self.image.get_height() * (1 - scale) / 2

        # overwrite img *using the orig img
        self.image = pygame.transform.scale_by(self.image_orig, self._scale)

    def rotate(self, angle) -> None:
        """
        Rotates the object by `angle` degrees around the object's center.
        :param float angle: object's angle of rotation in degrees;
            -180.0 < `angle` <= 180.0
        """
        assert isinstance(angle, float) and -180.0 < angle <= 180.0

        # change angle to satisfy its invar
        center: tuple[float, float] = self.center()
        self._angle += angle + 360.0
        self._angle %= 360.0

        # find x, y coor so that center is unchanged
        w: float = self.image_orig.get_width()
        h: float = self.image_orig.get_height()
        theta: float = math.radians(self._angle)

        x_offset: float = (-w * math.cos(theta) + h * math.sin(theta)) / 2
        y_offset: float = -(w * math.sin(theta) + h * math.cos(theta)) / 2

        self.xpos = center[0] + x_offset
        self.ypos = center[1] + y_offset

        # overwrite img *using the orig img
        self.image = pygame.transform.rotate(self.image_orig, self._angle)

    def rotozoom(self, angle, scale):
        """
        TODO
        """
        # FIXME coor updated incorrectly
        #  kinda fucked up here
        assert isinstance(angle, float) and -180.0 < angle <= 180.0
        assert isinstance(scale, float) and scale > 0.0

        # == rotate == #
        # change angle to satisfy its invar
        center: tuple[float, float] = self.center()
        self._angle += angle + 360.0
        self._angle %= 360.0

        # find x, y coor so that center is unchanged
        w: float = self.image.get_width()
        h: float = self.image.get_height()
        theta: float = math.radians(self._angle)

        x_offset: float = (-w * math.cos(theta) + h * math.sin(theta)) / 2
        y_offset: float = -(w * math.sin(theta) + h * math.cos(theta)) / 2

        self.xpos = center[0] + x_offset
        self.ypos = center[1] + y_offset

        # == resize == #
        self._scale *= scale
        self.xpos += self.image.get_width() * (1 - scale) / 2
        self.ypos += self.image.get_height() * (1 - scale) / 2

        # overwrite img *using the orig img
        self.image = pygame.transform.rotozoom(self.image_orig, self._angle, self._scale)

        raise NotImplementedError
