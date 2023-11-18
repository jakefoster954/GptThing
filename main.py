from clients.audio_output_client import AudioOutputClient
from clients.gpt_client import GptClient
from dotenv import dotenv_values
import logging
from services.audio_input_service import AudioInputService
from services.manual_input_service import ManualInputService
import argparse


if __name__ == '__main__':
    # Configure argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument(
        "-a", "--audio-input", help="use microphone to store input", dest="is_audio_input", action="store_true")
    args = parser.parse_args()

    logging_level = logging.INFO if args.verbose else logging.WARNING
    logging.basicConfig(level=logging_level)

    logger = logging.getLogger(__name__)

    # Load env values
    env = dotenv_values(".env")

    logger.info("Running")

    # Load personality for GPT
    with open("personalities/test_personality.txt") as file:
        personality = file.read()

    # Configure clients and services
    if args.is_audio_input:
        audio_input = AudioInputService()
    else:
        audio_input = ManualInputService()
    gpt = GptClient(env["GPT_API_KEY"], personality)
    audio_output = AudioOutputClient(env["ELEVENLABS_API_KEY"])

    while True:
        # Wakeup command
        audio_input.wake_up("hello")
        print("Tom is awake")

        # Ask a question
        query = ""
        while query == "":
            query = audio_input.speech_to_text()

        # Check if program should stop
        if query.lower() == "stop":
            break

        # Generate Gpt output
        response: str = gpt.get_response(query)
        print(response)

        # Output text as audio
        audio_output.play_audio(response, "Tom Goodman")

    logger.info("Execution complete")

