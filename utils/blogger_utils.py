import os

import dotenv

# Load environment variables
dotenv.load_dotenv()
GOOGLE_BLOGGER_API_KEY = os.environ.get("GOOGLE_BLOGGER_API_KEY")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_BLOGSPOT_ID = os.environ.get("GOOGLE_BLOGSPOT_ID")
# The file downloaded from the Google API Console
CLIENT_SECRETS_FILE = "scripts/credentials.json"


# ------------------- DO NOT DELETE! -------------------------------------- #
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
