import sys

sys.path.append(".")


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
