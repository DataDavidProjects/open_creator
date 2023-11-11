import os
import sys
from itertools import zip_longest

from dotenv import load_dotenv

sys.path.append(".")
from src.processing.text_processing import Blogger
from src.utils.file_operations import load_config
from utils.firebase_utils import list_files_in_folder


def initialize_blogger(project_name):
    """
    Initialize the Blogger class.
    Args:
        project_name (str): The name of the project.
    Returns:
        Blogger: An instance of the Blogger class.
    """
    load_dotenv()
    config = load_config(project_name)
    api_key = os.getenv("OPENAI_API_KEY")
    project_path = f"src/assets/data/{project_name}/blog"
    template_file_path = config["blogger"]["blog"]["template_file_path"].format(
        project_path
    )
    return (
        Blogger(
            api_key,
            tone=config["blogger"]["blog"]["tone"],
            template_file_path=template_file_path,
        ),
        config,
    )


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
    )  # Assuming cover is always the first image


def generate_blog_content(blogger, topic, aspects, promo_links):
    """
    Generate the main content of the blog.
    Args:
        blogger (Blogger): An instance of the Blogger class.
        topic (str): The overall topic of the blog post.
        aspects (list): A list of aspects or tuples with aspects and promo links.
        promo_links (list): A list of additional promotional links.
    Returns:
        tuple: Contains title, introduction, main content sections, and ending information of the blog.
    """
    return (
        blogger.generate_title(topic),
        blogger.generate_introduction(topic),
        blogger.generate_main_content(topic, aspects, promo_on=True),
        blogger.generate_ending(
            blogger.generate_main_content(topic, aspects, promo_on=True), promo_links
        ),
    )


def structure_blog_content(main_content_sections, image_urls, promo_links):
    """
    Update the blog sections with images and promotional links.
    Args:
        main_content_sections (list): A list of main content sections of the blog.
        image_urls (list): A list of image URLs.
        promo_links (list): A list of promotional links.
    Returns:
        list: Updated main content sections with images and promotional links.
    """
    for section, image_url, promo_link in zip_longest(
        main_content_sections, image_urls, promo_links, fillvalue=None
    ):
        if section:
            section["image_url"] = image_url if image_url else None
            section["promo_link"] = promo_link if promo_link else None
    return main_content_sections
