from clients.audio_input_client import AudioInputClient
from exceptions.audio_input_client_exceptions import AudioInputClientException
import logging


class AudioInputService:
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.client = AudioInputClient.instance()

    def wake_up(self, phrase: str) -> None:
        awake: bool = False
        while not awake:
            try:
                speech = self.client.speech_to_text()
                self.__logger.info("speech: %s", speech)
                if phrase.lower() in speech.lower():
                    awake = True
            except AudioInputClientException:
                pass

    def speech_to_text(self) -> str:
        try:
            text = self.client.speech_to_text()
            return text
        except AudioInputClientException:
            self.__logger.error("Error in Audio input client")
            return ""
