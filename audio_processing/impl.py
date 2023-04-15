import logging
from speech_recognition import Recognizer
from speech_recognition import AudioData

logger = logging.getLogger(__name__)


class VoiceProcessor:
    def __init__(self):
        self.recognizer = Recognizer()


class VoiceProcessorImpl(VoiceProcessor):

    def recognize(self, audio: AudioData) -> str:
        query = None
        try:
            logger.debug('Recognizing speech...')
            query = self.recognizer.recognize_google(audio, language='en_gb')
            logger.debug(f'The input speech was: {query}')
        except Exception as exception:
            print(exception)
        return query
