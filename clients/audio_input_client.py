from contextlib import contextmanager
from ctypes import *

import speech_recognition as sr

from exceptions.audio_input_client_exceptions import AudioInputClientException
from singleton import Singleton
import logging


@Singleton
class AudioInputClient:
    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

        def py_error_handler(filename, line, function, err, fmt):
            pass

        self.__c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

    @contextmanager
    def __noalsaerr(self):
        asound = cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(self.__c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)

    def speech_to_text(self) -> str:
        self.__logger.info("Running speech_to_text")
        try:
            with self.__noalsaerr():
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    r.adjust_for_ambient_noise(source=source, duration=1)
                    audio = r.listen(source=source)
                    text = r.recognize_google(audio)
                    self.__logger.info("Audio recognised: %s", text)
                    return text
        except sr.UnknownValueError:
            self.__logger.error("No speech detected.")
            raise AudioInputClientException("No speech detected")
        except sr.RequestError as e:
            self.__logger.error("Could not request results from the speech recognition service; {0}".format(e))
            raise AudioInputClientException("Could not request results from the speech recognition service")


if __name__ == "__main__":
    print("Start")
    f = AudioInputClient.instance()
    output = f.speech_to_text()
    print(output)
