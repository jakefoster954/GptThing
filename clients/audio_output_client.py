import logging
import elevenlabs
from elevenlabs import generate, stream, set_api_key


class AudioOutputClient:
    def __init__(self, api_key):
        self.__logger = logging.getLogger(__name__)
        elevenlabs.set_api_key(api_key)

    @staticmethod
    def get_voices() -> list[str]:
        return [voice.name for voice in elevenlabs.voices().voices if voice.name is not None]

    def play_audio(self, text: str, voice: str, model: str = "eleven_multilingual_v2") -> None:
        self.__logger.info("Running play_audio with content: %s", text)
        self.__logger.warning("This costs money!")

        if voice not in self.get_voices():
            self.__logger.error("%s is not recognised as a supported voice", voice)
            return

        self.__logger.info("Audio output config: %s %s", voice, model)

        audio_stream = generate(
            text=text,
            voice=voice,
            model=model,
            stream=True
        )

        stream(audio_stream)
