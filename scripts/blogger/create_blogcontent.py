import sys

sys.path.append(".")

import os
import time

# Usage example:
from dotenv import load_dotenv

from src.processing.text_processing import Blogger

# time start
start_time = time.time()


# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

# Initialize the Blogger class with the API key
blogger = Blogger(api_key, tone="Narrating")


# Define the topic for the blog post
topic = "Muay Thai"

# Generate parts of the blog post
title = blogger.generate_title(topic)
subtitle = blogger.generate_subtitle(topic)
introduction = blogger.generate_introduction(topic)

# Define the aspects for the blog post about Dubai, including promotional links where appropriate
aspects = [
    "Origins of Muay Thai",  # Regular section without promotion
    (
        "The equipment used",
        "https://eu.yokkao.com/it/collections/muay-thai-shorts",
    ),  # Section with promotion
    "The most important event of Muay Thai",
]

# Generate the main content, with promotions turned on
main_content = blogger.generate_main_content(topic, aspects, promo_on=True)

main_content = blogger.generate_main_content(topic, aspects)
recap = blogger.generate_recap(topic)
ending = blogger.generate_ending()

# time end
end_time = time.time()


# Execution time
print(f"Execution time: {end_time-start_time} seconds")

# Output the blog post
print(f"Title: {title}\n")
print(f"Subtitle: {subtitle}\n")
print(f"Introduction:\n{introduction}\n")
print(f"Main Content:\n{main_content}\n")
print(f"Recap:\n{recap}\n")
print(f"Ending:\n{ending}\n")


with open("blog_post.txt", "w", encoding="utf-8") as file:
    file.write(f"Title: {title}\n\n")
    file.write(f"Subtitle: {subtitle}\n\n")
    file.write(f"Introduction:\n{introduction}\n\n")
    file.write(f"Main Content:\n{main_content}\n\n")
    file.write(f"Recap:\n{recap}\n\n")
    file.write(f"Ending:\n{ending}\n")
