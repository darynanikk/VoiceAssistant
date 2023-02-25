from command import Settings
from service.keyboard import Keyboard
from service.keyboard.impl import KeyboardImpl


class KeyboardSettings(Settings):
    pass


class KeyboardCommand:

    def __init__(self):
        self._keyboard: Keyboard = KeyboardImpl()

        self._settings = KeyboardSettings()
