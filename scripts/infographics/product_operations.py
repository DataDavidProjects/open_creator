import os
import random
import shutil
from typing import List

from src.processing.image_processing import (
    create_grid_infographic,
    fill_transparency,
    pad_image_to_size,
    reduce_size,
)
from src.utils.file_operations import read_images


def create_product_grid(background_image_path: str, product_path: str, title: str):
    original_products = read_images(path=product_path)
    products = [
        pad_image_to_size(
            reduce_size(fill_transparency(img=i), size=(600, 600)), (650, 650)
        )
        for i in original_products
    ]

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
