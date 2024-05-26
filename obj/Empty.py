from obj.GameObject import GameObject


class Empty(GameObject):
    """
    An empty object; does not draw anything on the screen
    """
    def __init__(self):
        super().__init__(0.0, 0.0)

    def draw(self, screen) -> None:
        pass
