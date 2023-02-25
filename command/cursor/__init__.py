import os
from enum import Enum

from command import Settings
from service.cursor import Cursor
from service.cursor.impl import CursorImpl


class CursorSettings(Settings):

    def __init__(self, step: int, lookup_radius: int):
        super().__init__()
        self.step = step
        self.lookup_radius = lookup_radius


class CursorCommand:

    def __init__(self):
        self._cursor: Cursor = CursorImpl()

        step = os.environ.get('CURSOR_STEP_PX', 15)
        lookup_radius = os.environ.get('CURSOR_RADIUS_LOOKUP_PX', 200)
        self._settings = CursorSettings(step, lookup_radius)
