import unittest
from obj.GameObject import *


class GameObjectTest(unittest.TestCase):
    def test_center(self):
        game_object = GameObject(0.0, 0.0, "foo.png", True)
        center = game_object.center()
        self.assertAlmostEquals(25.0, center[0])
        self.assertAlmostEquals(50.0, center[1])

    def test_corners(self):
        """
        test for attribute `corners`
        """
        # NO ROTATION
        game_object = GameObject(0.0, 0.0, "foo.png", True)
        width = 50
        height = 100
        corners = self._list_of_tuples_to_int(game_object.get_corners())
        self.assertEqual([(0, 0), (width, 0), (0, height),
                          (width, height)], corners)

        # move down by 25.0 px
        game_object.move((False, False, True, False), 25.0)
        corners = self._list_of_tuples_to_int(game_object.get_corners())
        self.assertEqual([(0, 25), (width, 25),
                          (0, height + 25), (width, height + 25)], corners)

        # move to the right by 200.0 px
        game_object.move((False, False, False, True), 200.0)
        corners = self._list_of_tuples_to_int(game_object.get_corners())
        self.assertEqual([(200, 25), (width + 200, 25), (200, height + 25),
                          (width + 200, height + 25)], corners)

    def test_resize(self):
        """
        When object is resized, the center remains unchanged
        """
        game_object = GameObject(0.0, 0.0, "foo.png", True)
        # scale > 1
        self._test_resize_helper(game_object, 2.0)
        # scale < 1
        self._test_resize_helper(game_object, 0.5)
        # scale == 1
        self._test_resize_helper(game_object, 1.0)

    def test_rotate(self):
        """
        When object is rotated, the center remains unchanged and the corners of
        the object is represented by the equation
                    (x, y),
                    (x + w * cos, y + w * sin),
                    (x - h * sin, y + h * cos),
                    (x + w * cos - h * sin, y + w * sin + h * cos),
        where `x` is `xpos`, `y` is `ypos`, and `w` and `h` is the width and
        height of the object
        """
        game_object = GameObject(0.0, 0.0, "foo.png", True)
        self._test_rotate_helper(game_object, 50.0)
        self._test_rotate_helper(game_object, 100.0)
        self._test_rotate_helper(game_object, 150.0)

    @staticmethod
    def _list_of_tuples_to_int(tuples) -> list[tuple[int, int]]:
        """
        Converts all `float` in `tuples` into `int`
        :param list[tuple[float, float] tuples: the list to convert
        :return: a list with all entries of type `int`
        """
        assert isinstance(tuples, list)
        for i in tuples:
            assert isinstance(i, tuple) and len(i) == 2
            for j in i:
                assert isinstance(j, float)

        for i in range(len(tuples)):
            tuples[i] = (int(tuples[i][0]), int(tuples[i][1]))

        return tuples

    def _test_resize_helper(self, game_object: GameObject, scale: float) -> None:
        width = game_object.image_orig.get_width()
        height = game_object.image_orig.get_height()
        center = game_object.center()
        game_object.resize(scale)
        new_center = game_object.center()

        for i in range(2):
            self.assertAlmostEquals(center[i], new_center[i])

    def _test_rotate_helper(self, game_object: GameObject, angle: float) -> None:
        width = game_object.image_orig.get_width()
        height = game_object.image_orig.get_height()
        # center unchanged
        center = game_object.center()
        game_object.rotate(angle)
        new_center = game_object.center()
        corners = game_object.get_corners()

        for i in range(2):
            self.assertAlmostEquals(center[i], new_center[i])

        # testing corners
        theta = math.radians(game_object._angle) #TODO
        w_sin = width * math.sin(theta)
        w_cos = width * math.cos(theta)
        h_sin = height * math.sin(theta)
        h_cos = height * math.cos(theta)
        x = game_object.xpos
        y = game_object.ypos

        expected = [(x, y),
                    (x + w_cos, y + w_sin),
                    (x - h_sin, y + h_cos),
                    (x + w_cos - h_sin, y + w_sin + h_cos)]

        for i in range(4):
            for j in range(2):
                self.assertAlmostEquals(expected[i][j], corners[i][j])


if __name__ == '__main__':
    unittest.main()
