import sys

sys.path.append(".")


from authentications import GOOGLE_BLOGSPOT_ID, create_blog_post

# Path to your token.json file
TOKEN_JSON_FILE = "scripts/token.json"


def read_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# Use the function to read the HTML content
html_file_path = "scripts/blogger/blog.html"
content = read_html_file(html_file_path)
print(content)

title = "Dazzling Dubai: Where Dreams Come True"
response = create_blog_post(
    GOOGLE_BLOGSPOT_ID, title, content, token_json_file=TOKEN_JSON_FILE
)
print(response.json())  # To print the response from the API
