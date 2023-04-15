from .impl import VoiceProcessorImpl
from .supplier import VoiceSupplier
from .supplier.impl import VoiceSupplierImpl


class AudioProcessor:
    def __init__(self):
        self._supplier = VoiceSupplierImpl()
        self._processor = VoiceProcessorImpl()

    def process(self) -> str:
        return self._processor.recognize(self._supplier.supply())
