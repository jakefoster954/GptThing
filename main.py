from clients.audio_output_client import AudioOutputClient
from clients.gpt_client import GptClient
from dotenv import dotenv_values
import logging
from services.audio_input_service import AudioInputService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("Running")

    # Load env values
    env = dotenv_values(".env")

    # Load personality for GPT
    with open("personalities/test_personality.txt") as file:
        personality = file.read()

    audio_input = AudioInputService()
    audio_input.wake_up("hey")
    print("Tom is awake")

    # Ask a question
    query = ""
    while query is "":
        query = audio_input.speech_to_text()

    # Generate Gpt output
    gpt = GptClient(env["GPT_API_KEY"], personality)
    response: str = gpt.get_response(query)
    print(response)

    # Output text as audio
    audio_output = AudioOutputClient(env["ELEVENLABS_API_KEY"])
    # audio_output.play_audio(response, "Tom Goodman")

    logger.info("Execution complete")

