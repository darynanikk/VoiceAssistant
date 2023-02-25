from service.cursor import Cursor, ClickType
import pyautogui


class CursorImpl(Cursor):
    def __init__(self):
        self._delegate = pyautogui
        x, y = self._delegate.size()
        self.center_x, self.center_y = x // 2, y // 2

    def click(self, click_type: ClickType):
        self._delegate.click(button=click_type.value)

    def move_to_center(self):
        self.move_to(self.center_x, self.center_y)

    def move_left(self, px):
        self._delegate.move(-px, 0)

    def move_right(self, px):
        self._delegate.move(px, 0)

    def move_top(self, px):
        self._delegate.move(0, -px)

    def move_down(self, px):
        self._delegate.move(0, px)

    def move_to(self, x: int, y: int):
        self._delegate.moveTo(x, y)
