# ChatGPT Experimentation

## Setup
To configure the application, install the required packages and dependencies found in `packages.txt` and `requirements.txt`'

You will need to create a `.env` file in the solution root containing the following:
 
## Running
To run the application, execute the following from the solution root:

`python3 main.py`

| Environment Variable | Description                |
|----------------------|----------------------------|
| GPT_API_KEY          | API Key for ChatGpt API    |
| ELEVENLABS_API_KEY   | Api Key for ElevenLabs API |

The following arguments can be added to change the application's behaviour

| Argument  |               | Behaviour                      |
|-----------|---------------|--------------------------------|
| -v        | --verbose     | Display logs                   |
| -a        | --audio-input | Use microphone as input source |

## Note
This was created during a 8hr Hackathon.
