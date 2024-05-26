from threading import Thread
import pygame


class Event(Thread):
    def __init__(self):
        super().__init__()
        self._key = []
        self._running = True

    @property
    def get_key(self) -> list[int]:
        """

        :return:
        """
        return self._key

    @property
    def running(self) -> bool:
        """
        :return: True if object is running; False otherwise
        """
        return self._running

    @running.setter
    def running(self, running):
        """
        :param bool running: True if object is running
        """
        self._running = running

    def key_down(self):
        """
        Checks if a key was pressed
        :param int key: the key meant to be checked
        """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._key.append(event.key)

    def delete_key(self):
        self._key = []

    def run(self):
        while self._running:
            self.key_down()
