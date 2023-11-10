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
        {"storageBucket": GOOGLE_FIREBASE_BUCKET},
    )
    return None


def upload_firebase_storage(local_file, cloud_file):
    if not firebase_admin._apps:
        init_firebase_storage()

    bucket = storage.bucket()
    blob = bucket.blob(cloud_file)
    blob.upload_from_filename(local_file)
    return blob.public_url


def list_files_in_folder(folder_path=None):
    if not firebase_admin._apps:
        init_firebase_storage()

    bucket = storage.bucket()
    blobs = bucket.list_blobs(
        prefix=folder_path
    )  # Add delimiter="/" to list only immediate children
    urls = []

    for blob in blobs:
        if blob.name.endswith("/"):  # Skip directories
            continue
        blob.make_public()  # Make sure the file is publicly accessible
        urls.append(blob.public_url)

    return urls


# --------------------------------------------------------------------------#
# # Upload Example
# root_images_path = f"src/assets/data/{project_name}/blog/images/"
# project_name = "aesthetic_destinations"


# file_image = "aesthetic_destinations_light.png"
# local_file_path = root_images_path + file_image
# cloud_file_path = "file_image"
# upload_firebase_storage(local_file=local_file_path, cloud_file=cloud_file_path)
