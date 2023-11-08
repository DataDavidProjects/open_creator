import os
from pathlib import Path

import dotenv
from openai import OpenAI

# Load environment variables
dotenv.load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")


# client = OpenAI(api_key=api_key)
# speech_file_path = Path(__file__).parent / "speech.mp3"
# response = client.audio.speech.create(
#     model="tts-1-hd",
#     voice="echo",
#     input="Aint no sunshine when she is gone ...",
# )

# response.stream_to_file(speech_file_path)

from openai import OpenAI

client = OpenAI()

# response = client.images.generate(
#     model="dall-e-3",
#     prompt=prompt,
#     size="1024x1024",
#     quality="standard",
#     n=1,
# )

# image_url = response.data[0].url
# response.data[0].save(Path(__file__).parent / "test.jpg")

# print(image_url)


from PIL import Image

image = Image.open(Path(__file__).parent / "aesthetic_destinations_template_12.png")
