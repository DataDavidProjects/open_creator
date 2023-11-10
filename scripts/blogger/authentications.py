import os

import dotenv
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Load environment variables
dotenv.load_dotenv()
GOOGLE_BLOGGER_API_KEY = os.environ.get("GOOGLE_BLOGGER_API_KEY")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_BLOGSPOT_ID = os.environ.get("GOOGLE_BLOGSPOT_ID")
# The file downloaded from the Google API Console
CLIENT_SECRETS_FILE = "scripts/credentials.json"


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
        "isDraft": draft,
    }

    # Make the POST request to create a new blog post
    response = requests.post(url, headers=headers, json=data)
    return response
