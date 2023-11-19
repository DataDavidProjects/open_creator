import logging
import os
import random
from typing import List, Optional

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
                    pass
    elif os.path.isfile(path):
        # If the path is a file, load the image file
        try:
            img = Image.open(path)
            images.append(img)
        except Exception as e:
            pass
    else:
        pass

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


import os


def rename_file_type(path: str, extension: str = "png"):
    """
    Rename all files in the given directory to have the specified extension.

    Parameters:
    - path (str): The path to the directory containing the files.
    - extension (str): The new file extension type, default is 'png'.
    """
    for filename in os.listdir(path):
        name, ext = os.path.splitext(filename)
        if ext:  # if there is an extension
            new_filename = f"{name}.{extension}"
            os.rename(os.path.join(path, filename), os.path.join(path, new_filename))
            print(f"Renamed {filename} to {new_filename}")


def scan_for_files(directory: str, suffixes: List[str]) -> Optional[str]:
    """
    Scan the provided directory for files with the given suffixes and return a random file path if available.
    :param directory: Directory to scan for files.
    :param suffixes: List of file suffixes to look for.
    :return: Path to a random file with a given suffix if files are found, otherwise None.
    """
    files = [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]
    matched_files = [
        f for f in files if any(f.lower().endswith(suffix) for suffix in suffixes)
    ]

    if matched_files:
        return os.path.join(directory, random.choice(matched_files))
    return None
