import sys

sys.path.append(".")


import os
import time

from dotenv import load_dotenv

from src.processing.text_processing import Blogger
from src.utils.file_operations import load_config

# Config Project files
project_name = "aesthetic_destinations"
config = load_config(project_name)
project_path = f"src/assets/data/{project_name}/blog"

# time start
start_time = time.time()

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

# Initialize the Blogger class with the API key and specify the tone and template path
template_file_path = config["blogger"]["blog"]["template_file_path"].format(
    project_path
)
output_file_path = config["blogger"]["blog"]["output_file_path"].format(project_path)

# Init Blogger
blogger = Blogger(
    api_key,
    tone=config["blogger"]["blog"]["tone"],
    template_file_path=template_file_path,
)
topic = config["blogger"]["blog"]["topic"]
# Title
title = blogger.generate_title(topic)

# Intro
introduction = blogger.generate_introduction(topic)
aspects = config["blogger"]["blog"]["aspects"]
# Generate the main content, with promotions turned on
main_content_sections = blogger.generate_main_content(topic, aspects, promo_on=True)


print(main_content_sections)
# Promotion links
promo_links = [
    section.get("promo", {}).get("link", "")
    for section in main_content_sections
    if section.get("promo")
]

# Make sure each link is structured properly for the template
structured_promo_links = [
    {
        "href": section.get("promo", {}).get("link", ""),
        "text": section.get("promo", {}).get("alt_text", "Click me!"),
    }
    for section in main_content_sections
    if section.get("promo")
]

# Generate the recap and ending, using the main content sections to inform the promo link text generation and the ending content
ending_info = blogger.generate_ending(structured_promo_links, main_content_sections)

# Structure the blog content for rendering
blog_content = {
    "title": title,
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
