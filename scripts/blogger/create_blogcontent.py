import sys

sys.path.append(".")


import os
import time
from itertools import zip_longest

from dotenv import load_dotenv

from src.processing.text_processing import Blogger
from src.utils.file_operations import load_config
from utils.firebase_utils import list_files_in_folder

# Config Project files
project_name = "aesthetic_destinations"
config = load_config(project_name)
project_path = f"src/assets/data/{project_name}/blog"

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")


# time start
start_time = time.time()


# Initialize the Blogger class with the API key and specify the tone and template path
template_file_path = config["blogger"]["blog"]["template_file_path"].format(
    project_path
)
output_file_path = config["blogger"]["blog"]["output_file_path"].format(project_path)
# Fetch Yaml aspect and Promotion Links.
aspects_data = config["blogger"]["blog"]["aspects"]
aspects = []
for item in aspects_data:
    # Check if item is a list with two elements (interpreted as a tuple)
    if isinstance(item, list) and len(item) == 2:
        aspect_tuple = tuple(item)  # Convert the list to a tuple
        aspects.append(aspect_tuple)
    # If the item is a single string (just a topic without a promo link)
    elif isinstance(item, str):
        aspects.append(item)


# Init Blogger
blogger = Blogger(
    api_key,
    tone=config["blogger"]["blog"]["tone"],
    template_file_path=template_file_path,
)
topic = config["blogger"]["blog"]["topic"]

print("Writing Blog ...")
# Title
title = blogger.generate_title(topic)

# Intro
introduction = blogger.generate_introduction(topic)
# Generate the main content, with promotions turned on
main_content_sections = blogger.generate_main_content(topic, aspects, promo_on=True)


# Promotion links
promo_links = [
    section.get("promo", {}).get("link", "")
    for section in main_content_sections
    if section.get("promo")
]
# extra promo links
extra_promo_links = config["blogger"]["blog"].get("extra_promo_links", [])


# Generate the recap and ending, using the main content sections to inform the promo link text generation and the ending content
ending_info = blogger.generate_ending(main_content_sections, extra_promo_links)

# Fetch images from FIREBASE
n_sections = 4
image_urls = list_files_in_folder(f"Blog/{project_name}/")[:n_sections]
# Cover image temporarey set as first image of blog storage in firebase
cover = image_urls[0]
# Insert Images
for section, image_url in zip_longest(
    main_content_sections, image_urls, fillvalue=None
):
    section["image_url"] = image_url


# Structure the blog content for rendering
blog_content = {
    "title": title,
    "cover": cover,
    "introduction": introduction,
    "sections": main_content_sections,
    "ending": ending_info,
}

# Render the blog post and write it to an HTML file
blogger.render_blog_post(blog_content, template_file_path, output_file_path)

# time end
end_time = time.time()

# Execution time
print(f"Execution time: {end_time - start_time} seconds")
