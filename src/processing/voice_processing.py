import os

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
openaiclient = OpenAI(api_key=api_key)


def generate_voice_preset(text: str) -> dict:
    # Prompt for the chat model to analyze the text and suggest voice settings
    prompt = f"""You are expert of the ElevenLabs API and you Analyze this text and suggest the best voice settings:\n{text}\n"
        "You have the following parameters to change:\n"
        "- stability would have 11 possible values (0.0, 0.1, ..., 1.0)\n"
        "- similarity_boost would also have 11 possible values\n"
        "- style would have 12 possible values (11 plus the option of not setting it)\n"
        "- use_speaker_boost has 2 possible values (True or False)\n\n"
        "Consider these aspects:\n"
        "- similarity_boost: A number indicating how much the AI should mimic the learned voice.\n"
        "- stability: A number controlling the randomness and emotional range.\n"
        "- style: A number representing the exaggeration of the speaker's style.\n"
        "- use_speaker_boost: A boolean indicating whether to increase similarity to the original speaker.\n\n"
        "What would be the ideal settings for a voice that fits this text?"
         output a dictionary like structure like:
        {{
        'stability': 0.8,
        'similarity_boost': 0.6,
        'style': 0.2,
        'use_speaker_boost': True,
    }}"""

    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a program made to execute instructions without comments.",
            },
            {"role": "user", "content": prompt},
        ],
    }

    # Get the analyzed result from the chat model
    response = openaiclient.chat.completions.create(**payload)

    # Assuming the chat model returns a dictionary-like string of settings, convert it to a dictionary
    # This part needs to be implemented according to the specific format of the output from the chat model
    # The code below is a placeholder and needs to be adapted to your actual output format
    output = eval(response.choices[0].message["content"])
    return output


# print(generate_voice_preset(text="I am become death, the destroyer of worlds..."))


presets = {
    "narrative": {
        "stability": 0.8,
        "similarity_boost": 0.6,
        "style": 0.2,
        "use_speaker_boost": True,
    },
    "podcast_host": {
        "stability": 0.75,
        "similarity_boost": 0.5,
        "style": 0.6,
        "use_speaker_boost": True,
    },
    "news_reporter": {
        "stability": 0.9,
        "similarity_boost": 0.7,
        "style": 0.1,
        "use_speaker_boost": True,
    },
    "audiobook_reader": {
        "stability": 0.85,
        "similarity_boost": 0.55,
        "style": 0.3,
        "use_speaker_boost": True,
    },
    "elearning_tutor": {
        "stability": 0.82,
        "similarity_boost": 0.6,
        "style": 0.4,
        "use_speaker_boost": True,
    },
    "customer_service_rep": {
        "stability": 0.7,
        "similarity_boost": 0.5,
        "style": 0.7,
        "use_speaker_boost": True,
    },
    "animated_character": {
        "stability": 0.65,
        "similarity_boost": 0.3,
        "style": 0.9,
        "use_speaker_boost": True,
    },
    "virtual_assistant": {
        "stability": 0.88,
        "similarity_boost": 0.65,
        "style": 0.2,
        "use_speaker_boost": True,
    },
    "motivational_speaker": {
        "stability": 0.78,
        "similarity_boost": 0.6,
        "style": 0.8,
        "use_speaker_boost": True,
    },
    "meditation_guide": {
        "stability": 0.95,
        "similarity_boost": 0.8,
        "style": 0.1,
        "use_speaker_boost": True,
    },
    "conversational": {
        "stability": 0.7,
        "similarity_boost": 0.4,
        "style": 0.5,
        "use_speaker_boost": False,
    },
    "dramatic_narrator": {
        "stability": 0.6,
        "similarity_boost": 0.5,
        "style": 0.8,
        "use_speaker_boost": True,
    },
    "friendly_advisor": {
        "stability": 0.8,
        "similarity_boost": 0.5,
        "style": 0.3,
        "use_speaker_boost": False,
    },
    "professional_presenter": {
        "stability": 0.85,
        "similarity_boost": 0.7,
        "style": 0.2,
        "use_speaker_boost": True,
    },
    "comedic_performer": {
        "stability": 0.5,
        "similarity_boost": 0.4,
        "style": 1.0,
        "use_speaker_boost": False,
    },
    "corporate_trainer": {
        "stability": 0.9,
        "similarity_boost": 0.6,
        "style": 0.2,
        "use_speaker_boost": True,
    },
    "gaming_streamer": {
        "stability": 0.7,
        "similarity_boost": 0.3,
        "style": 0.7,
        "use_speaker_boost": False,
    },
    "tech_reviewer": {
        "stability": 0.75,
        "similarity_boost": 0.55,
        "style": 0.4,
        "use_speaker_boost": True,
    },
    "historical_documentary": {
        "stability": 0.9,
        "similarity_boost": 0.7,
        "style": 0.3,
        "use_speaker_boost": True,
    },
    "action_movie_trailer": {
        "stability": 0.6,
        "similarity_boost": 0.4,
        "style": 0.9,
        "use_speaker_boost": True,
    },
}


# # Convert the list of Voice instances to a list of dictionaries including expanding the labels
# voice_data = []
# for voice in voices:
#     # Start with the non-dict attributes
#     voice_dict = {
#         "voice_id": voice.voice_id,
#         "name": voice.name,
#         "category": voice.category,
#         "description": voice.description,
#         "preview_url": voice.preview_url,
#     }
#     # Add the label attributes
#     voice_dict.update(voice.labels)
#     voice_data.append(voice_dict)

# # Create a DataFrame
# df_voices = pd.DataFrame(voice_data)
