import pyautogui

from service.keyboard import Keyboard


class KeyboardImpl(Keyboard):

    def __init__(self):
        self._delegate = pyautogui

    def type(self, input: str):
        # interval should be taken from KeyboardSettings instance
        self._delegate.write(input, interval=0.25)
