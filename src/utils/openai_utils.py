from authentication import *
from openai import OpenAI

# Load environment variables
openai_client = OpenAI(api_key=OPENAI_API_KEY)


# openai_client = OpenAI(api_key=api_key)
# speech_file_path = Path(__file__).parent / "speech.mp3"
# response = openai_client.audio.speech.create(
#     model="tts-1-hd",
#     voice="echo",
#     input="Aint no sunshine when she is gone ...",
# )

# response.stream_to_file(speech_file_path)


# response = openai_client.images.generate(
#     model="dall-e-3",
#     prompt=prompt,
#     size="1024x1024",
#     quality="standard",
#     n=1,
# )

# image_url = response.data[0].url
# response.data[0].save(Path(__file__).parent / "test.jpg")

# print(image_url)


# image = Image.open(Path(__file__).parent / "aesthetic_destinations_template_12.png")