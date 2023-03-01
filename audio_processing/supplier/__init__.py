from speech_recognition import (Microphone, Recognizer)


class VoiceSupplier:
    def __init__(self):
        self.microphone = Microphone()
        self.recognizer = Recognizer()
