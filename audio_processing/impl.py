from audio_processing import VoiceProcessor
from speech_recognition import AudioData


class VoiceProcessorImpl(VoiceProcessor):
    def recognize(self, audio: AudioData) -> str:
        query = None
        try:
            print('Recognizing speech...')
            query = self.recognizer.recognize_google(audio, language='en_gb')
            print(f'The input speech was: {query}')
        except Exception as exception:
            print(exception)
        return query
