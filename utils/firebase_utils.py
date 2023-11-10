import firebase_admin
from firebase_admin import credentials, storage

project_name = "aesthetic_destinations"
local_file_path = (
    f"src/assets/data/{project_name}/blog/images/aesthetic_destinations_light.png"
)


# ------------------ FIREBASE AUTH------------------------------------------#


def init_firebase_storage(project_name="aesthetic_destinations"):
    cred = credentials.Certificate("scripts/firebase.json")
    firebase_admin.initialize_app(
        cred,
        {
            "storageBucket": f"gs://opencreator-1699308232742.appspot.com/Blog/{project_name}"
        },
    )
    return None


def upload_firebase_storage(local_file, cloud_file):
    bucket = storage.bucket()
    blob = bucket.blob(cloud_file)
    blob.upload_from_filename(local_file)
    return blob.public_url


# --------------------------------------------------------------------------#


cloud_file_path = ""
upload_firebase_storage(local_file=local_file_path, cloud_file=cloud_file_path)
