import os
from typing import List

from PIL import Image
from utils.file_operations import setup_logger

logger = setup_logger()


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


# Example Usage:
# For a single image file:
# images = read_images('path_to_image_file.jpg')

# For a directory:
# images = read_images('path_to_directory')
