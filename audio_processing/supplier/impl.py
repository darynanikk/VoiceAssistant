from audio_processing.supplier import VoiceSupplier
from speech_recognition import AudioData


class VoiceSupplierImpl(VoiceSupplier):
    def supply(self) -> AudioData:
        with self.microphone as source:
            audio = self.recognizer.listen(source)
        return audio
