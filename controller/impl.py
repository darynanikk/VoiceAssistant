import os
import logging
import openai
import pyautogui

from audio_processing import AudioProcessor
from typing import Dict
from command.cursor.impl import CursorClickingCommand, CursorMovementCommand
from command.keyboard.impl import KeyboardTypingCommand
from controller import ScreenSearcher, Controller, ScreenSearcherController
from service.cursor import CursorMovementType, ClickType

openai.api_key = os.environ.get('OPENAI_API_KEY', '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')


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
                mouse_controller.process(' '.join(query[1:]))

            if controller == 'search':
                search_controller = self._controllers.get(controller)
                search_controller.process(' '.join(query[1:]))

            if controller == 'type':
                type_controller = self._controllers.get(controller)
                type_controller.process(' '.join(query[1:]))

            if query[0] == 'stop':
                print('stopped')
                break


class MouseController(Controller):
    def __init__(self, audio_processor: AudioProcessor):
        super().__init__(audio_processor)
        self._clicking = CursorClickingCommand()
        self._movement = CursorMovementCommand()
        self.screen_searcher = ScreenSearcher()

    def process(self, query: str):
        #TODO
        query = query.split()
        if query[0] == 'move':

            if query[1] in ['up', 'down', 'left', 'right']:
                direction = CursorMovementType.get_by(query[1])
                self._movement.move(direction, 120)
            else:
                try:

                    pos, x, y = self.screen_searcher.find_by_str(''.join(query[1:]))
                    self._movement.move_to(x, y)
                except:
                    pass

                # #move next
                # while 'next' in self._audio_processor.process().lower().split():
                #     for

        if query[0] == 'click':

            if query[1] in ['middle', 'left', 'right']:
                click_type = ClickType.get_by(query[1])
                self._clicking.click(click_type)


class SearchController(Controller):
    def __init__(self, audio_processor: AudioProcessor):
        super().__init__(audio_processor)
        self._engine = os.environ.get('OPENAI_MODEL_ENGINE', 'text-davinci-003')

    def process(self, query: str):

        completion = openai.Completion.create(
            engine=self._engine,
            prompt=query,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        print(completion.get("choices")[0].get("text"))


class TypingController(Controller):

    def __init__(self, audio_processor: AudioProcessor):
        super().__init__(audio_processor)
        self._typing = KeyboardTypingCommand()

    def process(self, query: str):
        self._typing.type(query)


if __name__ == '__main__':
    selector = Selector()
    selector.listen()
