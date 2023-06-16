from command.keyboard import KeyboardCommand


class KeyboardTypingCommand(KeyboardCommand):

    def type(self, input: str):
        self._keyboard.type(input)


class KeyboardPressingCommand(KeyboardCommand):
    def press(self, input: str):
        self._keyboard.press(input)


class KeyboardHoldingCommand(KeyboardCommand):
    def hold(self, input: str):
        self._keyboard.hold(input)


class KeyboardHotKeyCommand(KeyboardCommand):
    def hotkey(self, *args):
        self._keyboard.hotkey(*args)