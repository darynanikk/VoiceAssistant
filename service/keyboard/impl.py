import pyautogui

from service.keyboard import Keyboard


class KeyboardImpl(Keyboard):

    def __init__(self):
        self._delegate = pyautogui

    def type(self, input: str):
        # interval should be taken from KeyboardSettings instance
        self._delegate.write(input, interval=0.25)

    def press(self, input: str):
        self._delegate.press(input)

    def hold(self, input: str):
        self._delegate.hold(input)

    def hotkey(self, *args):
        self._delegate.hotkey(*args)
