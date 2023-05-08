import os
import cv2
import pyautogui

from typing import Tuple
from audio_processing import AudioProcessor
from typing import List
from easyocr import Reader
from dotenv import load_dotenv

load_dotenv()


class ScreenSearcherController:
    def __init__(self):
        pyautogui.screenshot('screen.png')
        self.image = cv2.imread(os.getenv('IMAGE_PATH'))
        self.reader = Reader(['en'], gpu=True)

    def create_list_of_controls(self) -> List:
        results = self.reader.readtext(self.image)
        controls = []

        for bbox, text, prob in results:
            top_left, top_right, bottom_right, bottom_left = bbox
            controls.append((text, top_left[0], top_left[1]))
        return controls


class ScreenSearcher:

    @staticmethod
    def find_by_str(input: str) -> Tuple:
        control_position = 0
        screen_searcher_controller = ScreenSearcherController()
        controls = screen_searcher_controller.create_list_of_controls()

        for text, top_left_x, top_left_y in controls:
            control_position += 1
            print(text)
            if text.lower() == input.lower():
                print(text)
                return control_position, top_left_x, top_left_y
        raise Exception(f"Could not found control {input}")


class Controller:

    def __init__(self, audio_processor: AudioProcessor):
        self._audio_processor = audio_processor

    def process(self, query: str):
        pass


if __name__ == '__main__':
    screen_searcher = ScreenSearcher()
    x, y, z = screen_searcher.find_by_str('Makros')
    pyautogui.click(x, y)
