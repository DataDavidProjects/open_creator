import argparse
import os
import yaml


def load_params(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def create_directories(project: str):
    os.makedirs(f"./data/{project}", exist_ok=True)
    os.makedirs(f"./config/{project}", exist_ok=True)
    os.makedirs(f"./data/{project}/videos", exist_ok=True)
    os.makedirs(f"./data/{project}/videos/images", exist_ok=True)
    os.makedirs(f"./data/{project}/background", exist_ok=True)
    os.makedirs(f"./data/{project}/pins", exist_ok=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a project.")
    parser.add_argument("project", type=str, help="The name of the project")
    args = parser.parse_args()
    create_directories(args.project)
