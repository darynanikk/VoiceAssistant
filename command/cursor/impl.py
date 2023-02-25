from command.cursor import CursorCommand
from service.cursor import ClickType, CursorMovementType


class CursorClickingCommand(CursorCommand):

    def click(self, button: ClickType):
        self._cursor.click(button)


class CursorMovementCommand(CursorCommand):

    def move(self, direction: CursorMovementType):
        # TODO
        pass

    def move_to_center(self):
        self._cursor.move_to_center()

    def move_to(self, x: int, y: int):
        self._cursor.move_to(x, y)
