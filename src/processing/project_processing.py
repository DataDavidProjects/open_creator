import argparse
import os
import yaml


def load_params(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def create_directories(project: str):
    os.makedirs("data/videos", exist_ok=True)
    os.makedirs("data/videos/images", exist_ok=True)
    os.makedirs("fonts", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs(f"data/{project}", exist_ok=True)
    os.makedirs("data/background", exist_ok=True)
    os.makedirs("data/pins", exist_ok=True)


def ensure_correct_directory():
    if not os.path.basename(os.getcwd()) == "open_creator":
        print(
            "Please navigate to the 'open_creator' directory before running this script."
        )
        exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a project.")
    parser.add_argument("project", type=str, help="The name of the project")
    args = parser.parse_args()

    ensure_correct_directory()
    create_directories(args.project)
