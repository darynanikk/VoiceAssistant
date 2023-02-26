from command.cursor import CursorCommand
from service.cursor import ClickType, CursorMovementType


class CursorClickingCommand(CursorCommand):

    def click(self, button: ClickType):
        self._cursor.click(button)


class CursorMovementCommand(CursorCommand):

    def move(self, direction: CursorMovementType, px: int):
        if direction == CursorMovementType.LEFT:
            self._cursor.move_left(px)
        elif direction == CursorMovementType.RIGHT:
            self._cursor.move_right(px)
        elif direction == CursorMovementType.UP:
            self._cursor.move_top(px)
        elif direction == CursorMovementType.DOWN:
            self._cursor.move_down(px)

    def move_to_center(self):
        self._cursor.move_to_center()

    def move_to(self, x: int, y: int):
        self._cursor.move_to(x, y)
