import abc
import pyautogui
from enum import Enum


class ClickType(Enum):
    MIDDLE = "middle"
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def get_buy(cls, input_type):
        return cls[input_type]


class CursorMovementType(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def get_buy(cls, input_type):
        return cls[input_type]


class Settings:
    def __init__(self):
        pass


class CursorSettings:
    def __init__(self, step, lookup_radius):
        self.step = step
        self.lookup_radius = lookup_radius


class Cursor(abc.ABC):
    @abc.abstractmethod
    def click(self, click_type):
        pass

    @abc.abstractmethod
    def move_to_center(self):
        pass

    @abc.abstractmethod
    def move_left(self, px):
        pass

    @abc.abstractmethod
    def move_right(self, px):
        pass

    @abc.abstractmethod
    def move_top(self, px):
        pass

    @abc.abstractmethod
    def move_down(self, px):
        pass


class CursorImplementation(Cursor):
    def __init__(self):
        self.client = pyautogui
        x, y = self.client.size()
        self.center_x, self.center_y = x // 2, y // 2

    def click(self, click_type):
        self.client.click(button=click_type)

    def move_to_center(self):
        self.client.move(self.center_x, self.center_y)

    def move_left(self, px):
        self.client.move(-px, 0)

    def move_right(self, px):
        self.client.move(px, 0)

    def move_top(self, px):
        self.client.move(0, -px)

    def move_down(self, px):
        self.client.move(0, px)


if __name__ == "__main__":
    cursor = CursorImplementation()
    cursor.move_top(300)
