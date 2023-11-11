import sys

sys.path.append(".")

import os
import time
from itertools import zip_longest

from dotenv import load_dotenv

from src.processing.text_processing import Blogger, save_blog_content
from src.utils.file_operations import load_config
from utils.firebase_utils import list_files_in_folder

start_time = time.time()
# Config Project files
project_name = "aesthetic_destinations"
config = load_config(project_name)
project_path = f"src/assets/data/{project_name}/blog"

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # Use getenv for safety

# Initialize the Blogger class with the API key and template path
template_file_path = config["blogger"]["blog"]["template_file_path"].format(
    project_path
)
output_file_path = config["blogger"]["blog"]["output_file_path"].format(project_path)

# Fetch Yaml aspect and Promotion Links.
aspects = [
    tuple(item) if isinstance(item, list) else item
    for item in config["blogger"]["blog"]["aspects"]
]

# Fetch images from FIREBASE
firebase_imgs = list_files_in_folder(f"Blog/{project_name}/")
cover = firebase_imgs[0]  # Assuming cover is always the first image
image_urls = firebase_imgs[:]

# Init Blogger
blogger = Blogger(
    api_key,
    tone=config["blogger"]["blog"]["tone"],
    template_file_path=template_file_path,
)
topic = config["blogger"]["blog"]["topic"]

# Generate main content
print("Writing Blog ...")
title = blogger.generate_title(topic)
introduction = blogger.generate_introduction(topic)
main_content_sections = blogger.generate_main_content(topic, aspects, promo_on=True)

# Promotion links
promo_links = [
    section.get("promo", {}).get("link", "")
    for section in main_content_sections
    if section.get("promo")
]
extra_promo_links = config["blogger"]["blog"].get("extra_promo_links", [])

ending_info = blogger.generate_ending(main_content_sections, extra_promo_links)

# Insert Images
for section, image_url in zip_longest(
    main_content_sections, image_urls, fillvalue=None
):
    if section is not None:
        section["image_url"] = image_url

# Structure the blog content for rendering
blog_content = {
    "title": title,
    "introduction": introduction,
    "cover": cover,
    "sections": main_content_sections,
    "ending": ending_info,
}

# Save the blog content
save_file_path = project_path + "/tables/content.json"
save_blog_content(blog_content, save_file_path)

# Execution time
print(f"Execution time: {time.time() - start_time} seconds")
