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

        self.r = sr.Recognizer()

        try:
            with self.__noalsaerr():
                with sr.Microphone() as source:
                    self.r.dynamic_energy_threshold = False
                    self.r.energy_threshold = 1000
        except sr.UnknownValueError:
            self.__logger.error("No speech detected.")
            raise AudioInputClientException("No speech detected")
        except sr.RequestError as e:
            self.__logger.error("Could not request results from the speech recognition service; %s", e)
            raise AudioInputClientException("Could not request results from the speech recognition service")


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
                with sr.Microphone() as source:
                    self.__logger.info("Microphone being used")
                    audio = self.r.listen(source=source, timeout=2, phrase_time_limit=8)
                    self.__logger.info("Audio Received")
                    text = self.r.recognize_google(audio)
                    self.__logger.info("Audio recognised: %s", text)
                    return text
        except sr.UnknownValueError:
            self.__logger.error("No speech detected.")
            raise AudioInputClientException("No speech detected")
        except sr.WaitTimeoutError:
            self.__logger.error("No speech detected - Timed out.")
            raise AudioInputClientException("No speech detected - Timed out")
        except sr.RequestError as e:
            self.__logger.error("Could not request results from the speech recognition service; %s", e)
            raise AudioInputClientException("Could not request results from the speech recognition service")
