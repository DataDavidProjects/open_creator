import sys

sys.path.append(".")
import random
import time
import uuid

from src.processing.text_processing import Blogger
from src.utils.authentication import OPENAI_API_KEY, PROJECT_NAME, load_config
from src.utils.blogger_utils import (
    create_blog_post,
    get_title_from_html,
    render_blog_post,
    save_blog_content,
)
from src.utils.firebase_utils import list_files_in_folder


def read_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def fetch_images(project_name):
    """
    Fetch images from Firebase.
    Args:
        project_name (str): The name of the project.
    Returns:
        tuple: A list of image URLs and the cover image URL.
    """
    firebase_imgs = list_files_in_folder(f"Blog/{project_name}/")
    return (
        firebase_imgs[1:],
        firebase_imgs[0],
    )


# INIT PROJECT
CONFIG = load_config(project_name=PROJECT_NAME)


# Main Script
start_time = time.time()

# Config Project files
project_name = PROJECT_NAME
api_key = OPENAI_API_KEY
config = CONFIG
project_path = f"src/assets/data/{project_name}/blog"


blogger = Blogger(api_key=api_key)

# Fetch information of the blog
topic = config["blogger"]["blog"]["topic"]
print(topic)
aspects = config["blogger"]["blog"]["aspects"]
print(aspects)

n = 1
for _ in range(n):
    # Generate Content
    image_urls, cover = fetch_images(project_name)
    title = blogger.generate_title(topic=topic)
    introduction = blogger.generate_introduction(topic=topic)
    print(introduction)

    structured_sections = blogger.generate_main_content(aspects=aspects, seo=False)

    # Add Images to the main section
    for n, section in enumerate(structured_sections):
        image_url = random.sample(image_urls, 1)[0]
        section["image_url"] = image_url if image_url else None

    # Generate Ending
    ending = blogger.generate_recap(structured_sections)
    extra_promo_links = config["blogger"]["blog"]["extra_promo_links"]

    # Create Reference links
    reference_links = [
        {
            "promo_link": aspect.get("promo_link"),
            "text": blogger.generate_button_link(
                promo_link=aspect.get("promo_link"), topic=aspect.get("topic")
            ),
        }
        for aspect in (aspects + extra_promo_links)
    ]
    ending_structure = {
        "content": ending,
        "promo_links": reference_links,
    }
    # Prepare the blog content for rendering
    blog_content = {
        "title": title,
        "introduction": introduction,
        "cover": cover,
        "sections": structured_sections,
        "ending": ending_structure,
    }

    # Generate a unique ID
    unique_id = uuid.uuid4()

    # Save the blog content with a unique ID suffix in the filename
    save_blog_content(
        blog_content,
        f"src/assets/data/{project_name}/blog/tables/content_{unique_id}.json",
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
    GOOGLE_BLOGSPOT_ID = config["blogger"]["GOOGLE_BLOGSPOT_ID"]
    # Use the function to read the HTML content
    html_file_path = output_file_path
    content = read_html_file(html_file_path)

    title = get_title_from_html(content)

    response = create_blog_post(
        GOOGLE_BLOGSPOT_ID,
        title,
        content,
        token_json_file=TOKEN_JSON_FILE,
    )
    print(response.json())  # To print the response from the API
