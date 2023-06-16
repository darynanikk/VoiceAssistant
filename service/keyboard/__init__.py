import abc

import pyautogui


class Keyboard(abc.ABC):

    @abc.abstractmethod
    def type(self, input: str):
        pass

    @abc.abstractmethod
    def press(self, input: str):
        pass

    @abc.abstractmethod
    def hold(self, input: str):
        pass

    @abc.abstractmethod
    def hotkey(self, *args):
        pass