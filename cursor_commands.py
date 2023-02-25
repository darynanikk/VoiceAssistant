from cursor_settings import CursorSettings
from cursor import CursorImplementation
from enum import Enum


class CursorMovementType(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def get_buy(cls, input_type):
        return cls[input_type]


class CursorClickingCommand:
    def __init__(self):
        self.cursor = CursorImplementation()
        #TODO
       # self.settings = CursorSettings()

    def click(self, button):
        self.cursor.click(button)


class CursorMovementCommand:

    def __init__(self):
        self.cursor = CursorImplementation()
        #TODO
        #self.settings = CursorSettings

    def move(self, direction):
        # TODO
        pass

    def move_to_center(self):
        self.cursor.move_to_center()

    def move_to(self, x, y):
        self.cursor.client.moveTo(x, y)


if __name__ == "__main__":
    cvm = CursorMovementCommand()
    cvm.move_to(100, 300)