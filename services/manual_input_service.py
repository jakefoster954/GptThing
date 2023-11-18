import logging


class ManualInputService:
    def __init__(self):
        self.__logger = logging.getLogger(__name__)

    def wake_up(self, phrase: str) -> None:
        pass

    def speech_to_text(self) -> str:
        while True:
            query = input("> ")
            if query != "":
                return query

