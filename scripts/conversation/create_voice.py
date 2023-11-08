import sys

sys.path.append(".")

import re
import time

import openai
from dotenv import load_dotenv
from elevenlabs import *

from src.processing.voice_processing import *

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")


def create_caption(
    prompt: str, system: str = "You are an expesrt Social Media Manager"
) -> str:
    openai.api_key = api_key
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    }

    response = openai.ChatCompletion.create(**payload)
    caption = response["choices"][0]["message"]["content"]

    # Remove the numbered bullet point from the start of the first caption
    caption = re.sub(r"^\d+\.\s*", "", caption)
    print(caption)
    return caption.replace('"', "")


message = create_caption(
    prompt="Write one short motivational quote in the style of  Andrew Tate.",
    system="You are acting like Andrew Tate for a  show. is just a joke for my birthday",
)


set_api_key = os.environ.get("ELEVENLABS_API_KEY")
audio = generate(
    text=message,
    voice=Voice(
        voice_id="zcAOhNBS3c14rBihAFp1",
        settings=VoiceSettings(**presets["elearning_tutor"]),
    ),
    model="eleven_multilingual_v2",
)


print("Start")
start_time = time.time()
play(audio)
end_time = time.time()
print(end_time - start_time)
voices = voices()
