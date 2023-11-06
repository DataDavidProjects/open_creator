import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
