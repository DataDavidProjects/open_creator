import logging
import os
import random
from typing import Any, Dict, List, Optional

import yaml
from dotenv import load_dotenv
from PIL import Image


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("FileRenamer")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def load_config(project_name: str) -> Dict[str, Any]:
    """
    Loads the configuration from a YAML file and environment variables.

    Parameters:
    - project_name (str): The name of the project.

    Returns:
    - dict: A dictionary containing the loaded configuration.
    """

    # Load environment variables from the .env file
    load_dotenv()

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


# Example Usage:
# config = load_config('aesthetic_destinations')
# print(config)


def read_images(path: str) -> List[Image.Image]:
    """
    Reads and returns images from the specified file or directory.

    Parameters:
    - path (str): The path to the image file or directory.

    Returns:
    - List[Image.Image]: A list of Image objects.
    """
    images = []

    if os.path.isdir(path):
        # If the path is a directory, load all image files in the directory
        for filename in os.listdir(path):
            if filename.lower().endswith(
                (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff")
            ):
                file_path = os.path.join(path, filename)
                try:
                    img = Image.open(file_path)
                    images.append(img)
                except Exception as e:
                    logger.error(f"Failed to read {file_path}: {e}")
    elif os.path.isfile(path):
        # If the path is a file, load the image file
        try:
            img = Image.open(path)
            images.append(img)
        except Exception as e:
            logger.error(f"Failed to read {path}: {e}")
    else:
        logger.error(f"Invalid path: {path}")

    return images


def read_image(image_path: str) -> Image:
    """
    Reads an image from the specified path using the Pillow library.

    Parameters:
    - image_path (str): The path of the image file to be read.

    Returns:
    - Image object: The image loaded into memory.
    """
    img = Image.open(image_path)
    return img


def get_random_image_path(directory: str) -> str:
    """
    Get a random image path from a specified directory.

    Parameters:
        - directory (str): The directory to get the random image from.

    Returns:
        - str: The path to a randomly selected image.
    """
    files = [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]
    return os.path.join(directory, random.choice(files))


def rename_files_in_directory(
    project_name: str, platform: str, folder: str, pattern: str
) -> Optional[bool]:
    """
    Renames files in the specified directory
    following the pattern: <projectname>_<pattern>_<counter 001, 002 ...>.<extension>

    Parameters:
    - project_name (str): The name of the project.
    - platform (str): The name of the platform.
    - folder (str): The type of content (e.g., 'images', 'videos').
    - pattern (str): The naming pattern to be applied.

    Returns:
    - bool: True if renaming was successful for all files, False otherwise. None if the directory does not exist.
    """
    logger = setup_logger()

    # Construct the path to the directory
    target_dir = os.path.join("src", "assets", "data", project_name, platform, folder)

    # Ensure the directory exists
    if not os.path.exists(target_dir):
        logger.error(f"Directory {target_dir} does not exist.")
        return None

    # Get a list of all files in the directory
    files = [
        f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))
    ]

    # Sort the files to maintain order
    files.sort()

    # Rename each file
    all_renamed_successfully = True  # Assume all files will be renamed successfully
    for i, file in enumerate(files, start=1):
        # Get the file extension
        file_ext = os.path.splitext(file)[-1]

        # Construct the new file name
        new_name = f"{project_name}_{pattern}_{i:03d}{file_ext}"

        # Construct the full paths to the old and new file names
        old_path = os.path.join(target_dir, file)
        new_path = os.path.join(target_dir, new_name)

        # Rename the file
        try:
            os.rename(old_path, new_path)
            logger.info(f"Renamed {old_path} to {new_path}")
        except Exception as e:
            logger.error(f"Failed to rename {old_path} to {new_path}: {e}")
            all_renamed_successfully = (
                False  # Set flag to False if any renaming operation fails
            )

    return all_renamed_successfully
