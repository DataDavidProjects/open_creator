import sys

sys.path.append(".")

import os
import re

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
openaiclient = OpenAI(api_key=api_key)


def create_caption(
    prompt: str, system: str = "You are an expert Social Media Manager for Pinterest"
) -> str:
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
    }

    response = openaiclient.chat.completions.create(**payload)
    caption = response.choices[0].message.content

    # Remove the numbered bullet point from the start of the first caption
    caption = re.sub(r"^\d+\.\s*", "", caption)
    print(caption)
    return caption.replace('"', "")


def create_caption_bulk(prompt: str) -> pd.DataFrame:
    # Generate captions
    response = create_caption(
        prompt=prompt,
        system="You are an expert Social Media Manager for Pinterest and you provide captions separated by a \n",
    )
    captions_list = response.split("\n")
    # Remove the numbered bullet point from the start of each caption
    captions_list = [
        re.sub(r"^\d+\.\s*", "", caption).replace("\n", "") for caption in captions_list
    ]
    # Create a DataFrame to store the captions
    data = pd.DataFrame(captions_list, columns=["caption"])
    return data
