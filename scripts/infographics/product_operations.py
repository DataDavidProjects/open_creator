import os
import random
import shutil
from typing import List, Tuple

from PIL import Image

from src.processing.image_processing import (
    create_grid_infographic,
    fill_transparency,
    pad_image_to_size,
    reduce_size,
)
from src.utils.file_operations import read_images


def image_grid_processing(path: str):
    original_products = read_images(path=path)
    products = [
        pad_image_to_size(
            reduce_size(fill_transparency(img=i), size=(600, 600)), (650, 650)
        )
        for i in original_products
    ]
    return products


def create_product_grid(background_image_path: str, product_path: str, title: str):
    products = image_grid_processing(path=product_path)

    # Sample 9 images without replacement
    n = 9
    if len(products) >= n:
        image_list = random.sample(products, n)
    else:
        raise ValueError(
            f"Not enough images to sample: {len(products)} available, {n} required."
        )

    # Create the infographic
    infographic = create_grid_infographic(
        background_path=background_image_path,
        images=image_list,
        header_text=title,
        header_height=200,
        font_size=50,
        font_path="src/assets/fonts/Montserrat_700.ttf",
    )

    return infographic


def create_mix(
    categories: List[str], output_base: str, n: int = 9, destination_folder="products"
) -> None:
    """
    Creates a directory and populates it with a specified number of items randomly picked from given categories.

    Parameters:
    categories (List[str]): A list of category names to pick products from.
    output_base (str): The base directory where the content directory and product categories are located.
    n (int): The number of items to pick and copy into the mix directory.

    Returns:
    None
    """

    # Creating a new mix directory with a name based on the provided categories
    mix_dir_name = "Mix_" + "_".join(categories)
    mix_directory = os.path.join(output_base, destination_folder, mix_dir_name)
    os.makedirs(mix_directory, exist_ok=True)

    # Initialize a list to hold all product file paths
    all_products = []

    # Iterate over each category to collect file paths of products
    for cat in categories:
        cat_dir = os.path.join(output_base, destination_folder, cat)
        for prod in os.listdir(cat_dir):
            # Check if the path is a file, not a subdirectory
            if os.path.isfile(os.path.join(cat_dir, prod)):
                all_products.append((cat, prod))

    # Randomly sample products to be copied to the mix directory
    selected_products = random.sample(all_products, n)

    # Copy each selected product to the newly created mix directory
    for cat, product in selected_products:
        product_path = os.path.join(output_base, destination_folder, cat, product)
        shutil.copy(product_path, os.path.join(mix_directory, product))

    return selected_products


def image_collect(
    root: str,
    n: int,
    subdir: List[str],
    suffixes: List[str] = [".png", ".jpg", ".jpeg", ".bmp", ".gif"],
) -> List[Tuple[Image.Image, str]]:
    image_list = []
    # Dictionary to keep track of images in each subdirectory
    images_in_subdir = {s: [] for s in subdir}

    # Pre-populate the dictionary with available images in each subdir
    for sub in subdir:
        full_path = os.path.join(root, sub)
        if os.path.isdir(full_path):
            # List all files and filter by suffixes
            images_in_subdir[sub] = [
                f for f in os.listdir(full_path) if f.lower().endswith(tuple(suffixes))
            ]

    # Randomly select images from the pre-populated list
    while len(image_list) < n:
        print("Searching...")
        for sub in subdir:
            if images_in_subdir[sub]:  # If there are images left in this subdir
                chosen_file = random.choice(images_in_subdir[sub])
                images_in_subdir[sub].remove(
                    chosen_file
                )  # Remove the chosen file to prevent re-selection
                file_path = os.path.join(root, sub, chosen_file).replace("\\", "/")
                try:
                    with Image.open(file_path) as img:
                        image_list.append(
                            (
                                pad_image_to_size(
                                    reduce_size(
                                        fill_transparency(img=img),
                                        size=(600, 600),
                                    ),
                                    (650, 650),
                                ),
                                file_path,
                            )
                        )
                        if len(image_list) == n:
                            return image_list
                except Exception as e:
                    print(f"Failed to open file {file_path}: {e}")

    return image_list
