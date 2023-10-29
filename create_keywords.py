import os

import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")


def get_keywords(
    prompt: str, system: str = "You are an expert Social Media Manager for Pinterest"
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

    return caption.replace('"', "")


n = 30
prompt = f""" 
Write me the most important {n} seo keywords related to travel and luxury on tiktok for 
Dubai along their average number of search.
Do not made up things.
example:
1.keyword , number
"""
r = get_keywords(prompt=prompt)
print(r)
