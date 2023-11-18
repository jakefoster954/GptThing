import logging
from elevenlabs import generate, play


class AudioOutputClient:
    def __init__(self):
        self.__logger = logging.getLogger(__name__)

    def play_audio(self, text: str) -> None:
        self.__logger.info("Running play_audio with content: %s", text)
        self.__logger.warning("This costs money!")
        audio = generate(
            text=text,
            voice="Bella",
            model="eleven_monolingual_v1"
        )

        play(audio)