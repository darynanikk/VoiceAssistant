import logging

import pyautogui
from typing import Tuple

from audio_processing import AudioProcessor


class ScreenSearcher:
   # Refactor
   # TODO
   # CREATE QUEUE OF ENTRIES
    @staticmethod
    def find_by_str(input: str) -> Tuple:
        x, y = pyautogui.locateCenterOnScreen(input)
        return x, y


class Controller:

    def __init__(self, audio_processor: AudioProcessor):
        self._audio_processor = audio_processor

    def listen(self):
        # TODO choose command when listening
        pass


if __name__ == '__main__':
    image = pyautogui.screenshot(region=(80, 500, 70, 41))
    image.save('calc7key.png')
    (x, y) = ScreenSearcher.find_by_str('calc7key.png')
    pyautogui.click(x, y)
