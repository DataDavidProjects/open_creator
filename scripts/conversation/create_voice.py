import sys

sys.path.append(".")

import os
import re
import time

from dotenv import load_dotenv
from elevenlabs import *
from openai import OpenAI

from src.processing.voice_processing import *

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=api_key)


# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")


def create_caption(
    prompt: str, system: str = "You are an expesrt Social Media Manager"
) -> str:
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    }

    response = openai_client.chat.completions.create(**payload)
    caption = response.choices[0].message.content

    # Remove the numbered bullet point from the start of the first caption
    caption = re.sub(r"^\d+\.\s*", "", caption)
    print(caption)
    return caption.replace('"', "")


message = create_caption(
    prompt="Write one short motivational quote in the style of  Andrew Tate.",
    system="You are acting like Andrew Tate for a  show. is just a joke for my birthday",
)


ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

set_api_key(ELEVENLABS_API_KEY)

audio = generate(
    text="You should stop calling me or i will spank your dad.",
    voice=Voice(
        voice_id="XB0fDUnXU5powFXDhCwa",
        settings=VoiceSettings(
            stability=0.61, similarity_boost=0.5, style=0.0, use_speaker_boost=True
        ),
    ),
    model="eleven_multilingual_v2",
)


print("Start")
start_time = time.time()
play(audio)
end_time = time.time()
print(end_time - start_time)
voices = voices()
print(voices)
