from command.keyboard import KeyboardCommand


class KeyboardTypingCommand(KeyboardCommand):

    def type(self, input: str):
        self._keyboard.type(input)
