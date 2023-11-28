import json
import os

import requests
from bs4 import BeautifulSoup
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from jinja2 import Environment, FileSystemLoader, select_autoescape


def create_blog_post(blog_id, title, content, token_json_file, draft=True):
    # Load the saved credentials from token.json
    creds = None
    if os.path.exists(token_json_file):
        creds = Credentials.from_authorized_user_file(token_json_file)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise Exception("No valid credentials provided.")
    else:
        raise FileNotFoundError("Token.json file not found.")

    # Extract the access token from credentials
    access_token = creds.token

    # Set up the Blogger API request
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "kind": "blogger#post",
        "blog": {"id": blog_id},
        "title": title,
        "content": content,
    }

    # Make the POST request to create a new blog post
    response = requests.post(url, headers=headers, json=data)
    return response.json()


def get_title_from_html(html_content):
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the title tag and get its text content
    title_tag = soup.find("title")
    if title_tag:
        return title_tag.get_text()
    else:
        raise ValueError("No title tag found in HTML content.")


def save_blog_content(content, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=4)


def load_blog_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"No saved content found at {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while loading the blog content: {e}")
        return None


def render_blog_post(blog_content, template_file_path, output_file_path):
    # Extract the directory from the template file path
    template_dir = os.path.dirname(template_file_path)
    # If the directory is empty, it means a relative path was provided
    template_dir = template_dir if template_dir else "."

    # Set up the Jinja2 environment with the directory of the template file
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )

    # Now get the template by its filename only
    template_filename = os.path.basename(template_file_path)
    template = env.get_template(template_filename)

    # Render the template with the provided blog content
    html_content = template.render(blog_content)

    # Use BeautifulSoup to pretty-print the HTML
    soup = BeautifulSoup(html_content, "html.parser")
    formatted_html = soup.prettify()
    html_content = formatted_html

    # Write the formatted HTML content to the output file with UTF-8 encoding
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(html_content)


def read_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def retrieve_blog_posts(blog_id, token_json_file):
    """
    Retrieve the blog posts using Blogger API, using credentials from a token json file.
    Parameters:
    - blog_id: str. The ID of the blog for which to retrieve posts.
    - token_json_file: str. The file path of the token json file with credentials.
    Returns:

    - response: requests.Response. The response from the API call.
    """
    # Load the saved credentials from token.json
    creds = None
    if os.path.exists(token_json_file):
        creds = Credentials.from_authorized_user_file(token_json_file)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise Exception("No valid credentials provided.")
    else:
        raise FileNotFoundError("Token.json file not found.")
    # Extract the access token from credentials
    access_token = creds.token
    # Set up the Blogger API request
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"
    headers = {"Authorization": f"Bearer {access_token}"}
    # Make the GET request to retrieve blog posts
    return requests.get(url, headers=headers).json()


def get_last_blog_post_info(response_json):
    """
    Retrieve the URL and ID of the last blog post from a Blogger API JSON response.

    Parameters:
    - response_json: dict. A JSON response from the Blogger API containing blog posts.

    Returns:
    - tuple: A tuple containing the URL and ID of the last blog post.
    """
    # Retrieve the last blog post from the items list
    last_blog_post = response_json["items"][-1] if response_json.get("items") else None

    # Extract the URL and ID if the post is available
    last_blog_post_url = last_blog_post.get("url") if last_blog_post else None
    last_blog_post_id = last_blog_post.get("id") if last_blog_post else None

    return last_blog_post_url, last_blog_post_id
