import abc
from enum import Enum


class CursorMovementType(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def get_by(cls, type: str):
        for item in CursorMovementType:
            if item.name.lower() == type.lower():
                return item

        raise Exception(f"Could not convert {type} to value from list {list(cls)}")


class ClickType(Enum):
    MIDDLE = "middle"
    LEFT = "left"
    RIGHT = "right"

    @classmethod
    def get_by(cls, type: str):
        for item in ClickType:
            if item.name.lower() == type.lower():
                return item

        raise Exception(f"Could not convert {type} to value from list {list(cls)}")


class Cursor(abc.ABC):

    @abc.abstractmethod
    def click(self, click_type: ClickType):
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

    @abc.abstractmethod
    def move_to(self, x: int, y: int):
        pass
