import sys

sys.path.append(".")


import json
import os
from typing import *

import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_BLOGGER_API_KEY = os.environ.get("GOOGLE_BLOGGER_API_KEY")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_BLOGSPOT_ID = os.environ.get("GOOGLE_BLOGSPOT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_FONT_API_KEY = os.getenv("GOOGLE_FONT_API_KEY")


PINTEREST_APP_ID = os.getenv("PINTEREST_APP_ID")
PINTEREST_APP_SECRET = os.getenv("PINTEREST_APP_SECRET")

# The file downloaded from the Google API Console
CLIENT_SECRETS_FILE = "scripts/credentials.json"


PROJECT_NAME = "theallurecode"


def load_config(project_name: str) -> Dict[str, Any]:
    """
    Loads the configuration from a YAML file and environment variables.

    Parameters:
    - project_name (str): The name of the project.

    Returns:
    - dict: A dictionary containing the loaded configuration.
    """

    # Construct the path to the YAML configuration file
    config_file_path = os.path.join("src", "config", f"{project_name}.yaml")

    # Ensure the YAML configuration file exists
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(
            f"Configuration file {config_file_path} does not exist."
        )

    # Load the YAML configuration file
    with open(config_file_path, "r") as file:
        config = yaml.safe_load(file)

    # Merge the loaded environment variables into the configuration dictionary
    # This allows environment variables to override values specified in the YAML file
    config.update(os.environ)

    return config


# -------------------BLOGGER API AUTH -------------------------------------- #
# # The scope for the Blogger API
# SCOPES = ["https://www.googleapis.com/auth/blogger"]

# # Create the flow using the client secrets file and the scopes
# flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)

# # Run the flow to get the credentials
# # Depending on the library version, this might be run_local_server() or run_desktop()
# flow.run_local_server()

# # Save the credentials for the next run
# with open("token.json", "w") as token:
#     token.write(flow.credentials.to_json())
# ------------------------------------------------------------------------#


# ---------------------- PINTEREST API AUTH ------------------------------------#
# TUTORIAL : https://www.youtube.com/watch?v=4MSGXHtcpsM

from base64 import b64encode

# https://www.base64encode.org/
import requests


def get_pinterest_credentials(
    client_id: str,
    client_secret: str,
    your_code: str,
    redirect_uri="https://www.dataprojects.cloud/",
    file_path="scripts/pinterest_dataprojects.json",
):
    """
    Function to get an access token from Pinterest.

    Parameters:
    client_id (str): Your Pinterest Application client ID.
    client_secret (str): Your Pinterest Application client secret.
    your_code (str): The code you received from Pinterest after authorization.

    Returns:
    str: Access token, if the request was successful; otherwise, it returns an error message.
    """

    # Encode the client ID and client secret to Base64 format as required for the header.
    credentials = f"{client_id}:{client_secret}"
    base64_encoded_credentials = b64encode(credentials.encode()).decode()

    # Prepare the headers.
    headers = {
        "Authorization": f"Basic {base64_encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # Prepare the data.
    data = {
        "grant_type": "authorization_code",
        "code": your_code,
        "redirect_uri": redirect_uri,
    }

    # Make the POST request to get the token.
    response = requests.post(
        "https://api.pinterest.com/v5/oauth/token", headers=headers, data=data
    )

    # Check if the request was successful and return the token or error message.
    try:
        with open(file_path, "w") as file:
            json.dump(response.json(), file)
        return json
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")
        return None


# ------------------------------------------------------------------------------#

USER = "theallurecode"
response = get_pinterest_credentials(
    PINTEREST_APP_ID,
    PINTEREST_APP_SECRET,
    your_code="91745d477b40802ffeb04a4636de78bb58469ad3",
    file_path=f"src/utils/credential_pinterest_{USER}.json",
)
