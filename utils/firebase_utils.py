import dotenv
import firebase_admin
from firebase_admin import credentials, storage

from src.utils.file_operations import load_config

# Load environment variables
dotenv.load_dotenv()
# Config Project files
project_name = "aesthetic_destinations"
config = load_config(project_name)
project_path = f"src/assets/data/{project_name}/blog"


# ------------------ FIREBASE AUTH------------------------------------------#
GOOGLE_FIREBASE_BUCKET = config["GOOGLE_FIREBASE_BUCKET"]


def init_firebase_storage(project_name="aesthetic_destinations"):
    cred = credentials.Certificate("scripts/firebase.json")
    firebase_admin.initialize_app(
        cred,
        {"storageBucket": f"{GOOGLE_FIREBASE_BUCKET}/Blog/{project_name}"},
    )
    return None


def upload_firebase_storage(local_file, cloud_file):
    bucket = storage.bucket()
    blob = bucket.blob(cloud_file)
    blob.upload_from_filename(local_file)
    return blob.public_url


# --------------------------------------------------------------------------#
# # Upload Example
# root_images_path = f"src/assets/data/{project_name}/blog/images/"
# project_name = "aesthetic_destinations"


# file_image = "aesthetic_destinations_light.png"
# local_file_path = root_images_path + file_image
# cloud_file_path = "file_image"
# upload_firebase_storage(local_file=local_file_path, cloud_file=cloud_file_path)
