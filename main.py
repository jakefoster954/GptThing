from clients.gpt_client import GptClient
from dotenv import dotenv_values
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("Running")

    # Load env values
    env = dotenv_values(".env")

    # Load personality for GPT
    with open("personalities/test_personality.txt") as file:
        personality = file.read()

    # Generate Gpt output
    gpt = GptClient(env["GPT_API_KEY"], personality)
    query: str = "What is the capital of Hungary?"
    response: str = gpt.get_response(query)
    print(response)

    logger.info("Execution complete")

