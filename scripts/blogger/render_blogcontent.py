import sys

sys.path.append(".")

import time

from src.processing.text_processing import load_blog_content, render_blog_post
from src.utils.file_operations import load_config

start_time = time.time()
# Config Project files
project_name = "aesthetic_destinations"
config = load_config(project_name)
project_path = f"src/assets/data/{project_name}/blog"


# Initialize the Blogger class with the API key and template path
template_file_path = config["blogger"]["blog"]["template_file_path"].format(
    project_path
)
output_file_path = config["blogger"]["blog"]["output_file_path"].format(project_path)

# render template:
save_file_path = project_path + "/tables/content.json"
blog_content = load_blog_content(save_file_path)
render_blog_post(blog_content, template_file_path, output_file_path)
