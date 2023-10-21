import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Pinterest access token from environment variable
ACCESS_TOKEN = os.getenv("PINTEREST_ACCESS_TOKEN")

from pinterest.client import PinterestSDKClient

# Assuming you have a client created with your access token
client = PinterestSDKClient.create_client_with_token(ACCESS_TOKEN)
