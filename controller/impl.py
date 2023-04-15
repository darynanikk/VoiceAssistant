from audio_processing import AudioProcessor
from typing import Dict
from command.cursor.impl import CursorClickingCommand, CursorMovementCommand
from command.keyboard.impl import KeyboardTypingCommand
from controller import ScreenSearcher, Controller
from service.cursor import CursorMovementType


class Selector:

    def __init__(self):
        self._processor = AudioProcessor()
        self._controllers: Dict[str, Controller] = {'mouse': MouseController(), 'type': TypingController(),
                                                    'search': SearchController()}

    def listen(self) -> None:
        while True:
            query = self._processor.process().lower().split()

            if query[0] == 'move':
                mouse_controller = self._controllers.get('mouse')
                mouse_controller.move()

            if query[0] == 'stop':
                print('stopped')
                break


class MouseController(Controller):
    def __init__(self):
        super().__init__()
        self._clicking = CursorClickingCommand()
        self._movement = CursorMovementCommand()
        self.screen_searcher = ScreenSearcher()

    def listen(self):
        # TODO choose command when listening
        pass


class SearchController(Controller):
    # ChatGPT or simple (Wikipedia, StackOverFlow, Google)
    pass


class TypingController(Controller):
    def __init__(self):
        super().__init__()
        self._typing = KeyboardTypingCommand()

    def listen(self):
        pass


if __name__ == '__main__':
    selector = Selector()
    selector._controllers.get('mouse').move()
    selector._controllers.get('type').type_input("hello")
