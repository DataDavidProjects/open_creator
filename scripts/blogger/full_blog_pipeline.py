import sys

sys.path.append(".")
import time
import uuid

from create_blogcontent import *

from src.processing.text_processing import render_blog_post, save_blog_content


def read_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# Main Script
start_time = time.time()

# Config Project files
project_name = "aesthetic_destinations"
project_path = f"src/assets/data/{project_name}/blog"


title = "This is why you should come to Dubai..."

# Initialize Blogger
blogger, config = initialize_blogger(project_name)
# Fetch images and aspects
image_urls, cover = fetch_images(project_name)
aspects = [
    tuple(item) if isinstance(item, list) else item
    for item in config["blogger"]["blog"]["aspects"]
]
# Generate main content
print("Writing Blog ...")
title, introduction, main_content_sections, ending_info = generate_blog_content(
    blogger,
    config["blogger"]["blog"]["topic"],
    aspects,
    config["blogger"]["blog"].get("extra_promo_links", []),
)
# Structure the blog content with images and promotional links
structured_sections = structure_blog_content(
    main_content_sections,
    image_urls,
    config["blogger"]["blog"].get("extra_promo_links", []),
)
# Prepare the blog content for rendering
blog_content = {
    "title": title,
    "introduction": introduction,
    "cover": cover,
    "sections": structured_sections,
    "ending": ending_info,
}
# Generate a unique ID
unique_id = uuid.uuid4()

# Save the blog content with a unique ID suffix in the filename
save_blog_content(
    blog_content, f"src/assets/data/{project_name}/blog/tables/content_{unique_id}.json"
)

# Execution time
print(f"Execution time: {time.time() - start_time} seconds")


# Render blog
template_file_path = config["blogger"]["blog"]["template_file_path"].format(
    project_path
)
output_file_path = config["blogger"]["blog"]["output_file_path"].format(
    project_path, unique_id
)


render_blog_post(
    blog_content,
    template_file_path=template_file_path,
    output_file_path=output_file_path,
)


# Post Blog
# Path to your token.json file
TOKEN_JSON_FILE = "scripts/token.json"

# # Use the function to read the HTML content
# html_file_path = config["blogger"]["blog"]["output_file_path"].format(project_path)
# content = read_html_file(html_file_path)

# get_title_from_html(content)

# response = create_blog_post(
#     GOOGLE_BLOGSPOT_ID, title, content, token_json_file=TOKEN_JSON_FILE
# )
# print(response.json())  # To print the response from the API
