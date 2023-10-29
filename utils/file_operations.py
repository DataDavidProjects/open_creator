import logging
import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv


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


def rename_files(project_name: str, platform: str) -> Optional[bool]:
    """
    Renames files in the specified project and platform directory
    following the pattern: <projectname>_template_<counter 001, 002 ...>.png

    Parameters:
    - project_name (str): The name of the project.
    - platform (str): The name of the platform.

    Returns:
    - bool: True if renaming was successful for all files, False otherwise. None if the directory does not exist.
    """
    logger = setup_logger()

    # Construct the path to the templates directory
    templates_dir = os.path.join("assets", "data", project_name, platform, "templates")

    # Ensure the directory exists
    if not os.path.exists(templates_dir):
        logger.error(f"Directory {templates_dir} does not exist.")
        return None

    # Get a list of all files in the templates directory
    files = [
        f
        for f in os.listdir(templates_dir)
        if os.path.isfile(os.path.join(templates_dir, f))
    ]

    # Sort the files to maintain order
    files.sort()

    # Rename each file
    all_renamed_successfully = True  # Assume all files will be renamed successfully
    for i, file in enumerate(files, start=1):
        # Construct the new file name
        new_name = f"{project_name}_template_{i:03d}.png"

        # Construct the full paths to the old and new file names
        old_path = os.path.join(templates_dir, file)
        new_path = os.path.join(templates_dir, new_name)

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


# Example Usage:
# success = rename_files('my_project', 'instagram')
# if success is not None:
#     print(f"All files renamed successfully: {success}")


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
    config_file_path = os.path.join("config", f"{project_name}.yaml")

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
