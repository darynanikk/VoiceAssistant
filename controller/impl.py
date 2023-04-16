import logging

from audio_processing import AudioProcessor
from typing import Dict
from command.cursor.impl import CursorClickingCommand, CursorMovementCommand
from command.keyboard.impl import KeyboardTypingCommand
from controller import ScreenSearcher, Controller
from service.cursor import CursorMovementType


class Selector:

    def __init__(self):
        self._processor = AudioProcessor()
        self._controllers: Dict[str, Controller] = {'mouse': MouseController(self._processor),
                                                    'type': TypingController(self._processor),
                                                    'search': SearchController(self._processor)}

    def listen(self) -> None:
        while True:
            query = self._processor.process().lower().split()

            controller = query[0]
            if controller == 'mouse':
                mouse_controller = self._controllers.get(controller)
                mouse_controller.listen()

            if query[0] == 'stop':
                print('stopped')
                break


class MouseController(Controller):
    def __init__(self, audio_processor: AudioProcessor):
        super().__init__(audio_processor)
        self._clicking = CursorClickingCommand()
        self._movement = CursorMovementCommand()
        self.screen_searcher = ScreenSearcher()

    def listen(self):
        query = self._audio_processor.process().lower().split()

        command = query[0]
        if command == 'move':
            direction = CursorMovementType.get_by(query[1])
            self._movement.move(direction, 120)


class SearchController(Controller):
    # ChatGPT or simple (Wikipedia, StackOverFlow, Google)
    pass


class TypingController(Controller):

    def __init__(self, audio_processor: AudioProcessor):
        super().__init__(audio_processor)
        self._typing = KeyboardTypingCommand()

    def listen(self):
        pass


if __name__ == '__main__':
    selector = Selector()
    selector.listen()
    # selector._controllers.get('mouse').move()
    # selector._controllers.get('type').type_input("hello")
