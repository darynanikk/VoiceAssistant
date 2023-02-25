import abc

import pyautogui


class Keyboard(abc.ABC):

    @abc.abstractmethod
    def type(self, input: str):
        pass
