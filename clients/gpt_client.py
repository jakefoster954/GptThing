import logging
from openai import OpenAI
from openai.types.chat import ChatCompletion
from dotenv import dotenv_values


class GptClient:
    __logger = logging.getLogger(__name__)
    __history: list[(str, str)] = []
    __memory_size = 3

    def __init__(self, api_key: str, instructions: str, model: str = "gpt-3.5-turbo"):
        self.__client = OpenAI(
            api_key=api_key,
        )
        self.__instructions = instructions
        self.__model = model

    def get_response_mock(self, query: str) -> str:
        self.__logger.info("Running get_response_mock with content: %s", query)
        return "The capital of Indonesia is Jakarta."

    def get_response(self, query: str):
        self.__logger.info("Running get_response with content: %s", query)
        self.__logger.warning("This costs money!")

        messages = [
            {"role": "system", "content": self.__instructions},
        ]

        for (q, r) in self.__history[-self.__memory_size:]:
            messages.append({"role": "user", "content": q})
            messages.append({"role": "assistant", "content": r})

        messages.append({"role": "user", "content": query})

        chat_completion: ChatCompletion = self.__client.chat.completions.create(
            messages=messages,
            model=self.__model,
        )
        response: str = chat_completion.choices[0].message.content

        self.__history.append((query, response))

        return response
