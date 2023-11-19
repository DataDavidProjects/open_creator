import sys

sys.path.append(".")
import dotenv
import firebase_admin
from firebase_admin import credentials, storage

from src.utils.authentication import PROJECT_NAME, load_config

# Load environment variables
dotenv.load_dotenv()
# Config Project files
project_name = PROJECT_NAME
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
# project_name =  PROJECT_NAME


# file_image = "aesthetic_destinations_light.png"
# local_file_path = root_images_path + file_image
# cloud_file_path = "file_image"
# upload_firebase_storage(local_file=local_file_path, cloud_file=cloud_file_path)


def get_image_firebase(folder_path=None, image_name=None):
    if not firebase_admin._apps:
        init_firebase_storage()  # Replace with your method to initialize Firebase

    # Get the Firebase storage bucket
    bucket = storage.bucket()
    print(bucket)
    # Create the full path to the image file
    image_path = f"{folder_path}/{image_name}" if folder_path else image_name
    print(image_path)

    # Get the blob for the specific image
    blob = bucket.blob(image_path)

    if blob.exists():  # Check if the blob exists
        blob.make_public()  # Make sure the file is publicly accessible
        return blob.public_url
    else:
        return None  # Return None if the image does not exist
