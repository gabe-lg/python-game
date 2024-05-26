import unittest
from obj.Text import *


class TextTest(unittest.TestCase):
    def test_centering(self):
        # rectangle with width 100 and height 50
        pygame.init()
        screen = pygame.surface.Surface((100.0, 50.0))
        text = Text("foo", 0.0, 0.0, "Arcade.ttf", 50, (0, 0, 0), True)
        text.place(screen)
        center = text.center()
        self.assertAlmostEquals(50.0, center[0])
        self.assertAlmostEquals(25.0, center[1])

        # rectangle with width 0.01 and height 1000.0
        # test rounding
        pygame.init()
        screen = pygame.surface.Surface((0.01, 1000.0))
        text = Text("foo", 0.0, 0.0, "Arcade.ttf", 50, (0, 0, 0), True)
        text.place(screen)
        center = text.center()
        self.assertAlmostEquals(0.0, center[0])
        self.assertAlmostEquals(500.0, center[1])


if __name__ == '__main__':
    unittest.main()
