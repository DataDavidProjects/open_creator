import sys

sys.path.append(".")


from authentications import GOOGLE_BLOGSPOT_ID, create_blog_post

from src.processing.text_processing import get_title_from_html
from src.utils.file_operations import load_config

# Config Project files
project_name = "aesthetic_destinations"
config = load_config(project_name)
project_path = f"src/assets/data/{project_name}/blog"

# Path to your token.json file
TOKEN_JSON_FILE = "scripts/token.json"


def read_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# Use the function to read the HTML content
html_file_path = config["blogger"]["blog"]["output_file_path"].format(project_path)
content = read_html_file(html_file_path)


title = get_title_from_html(content)
response = create_blog_post(
    GOOGLE_BLOGSPOT_ID, title, content, token_json_file=TOKEN_JSON_FILE
)
print(response.json())  # To print the response from the API
