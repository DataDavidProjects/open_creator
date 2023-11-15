import os
import random
import sys

sys.path.append(".")
from src.processing.image_processing import (
    create_grid_infographic,
    fill_transparency,
    pad_image_to_size,
    reduce_size,
)
from src.utils.authentication import GOOGLE_BLOGGER_API_KEY
from src.utils.file_operations import read_images

project_name = "theallurecode"


def create_product_grid(background_image_path: str, product_path: str, title: str):
    original_products = read_images(path=product_path)
    products = [
        pad_image_to_size(
            reduce_size(fill_transparency(img=i), size=(400, 400)), (500, 500)
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
        font_path="arialbd.ttf",
    )

    return infographic


title_mapping = {
    "Fragrance": [
        "Essence of Irresistibility",
        "Charisma in a Bottle",
        "Scented Spell of Attraction",
        "Mystique Aromatics",
        "Perfumed Persuasion",
        "Aromatic Allure",
        "The Scent of Enchantment",
        "Captivating Fragrance Fusion",
        "Eau de Magnetism",
        "Whisper of Seduction",
    ],
    "Skincare": [
        "Clear Skin Essentials",
        "Uncomplicated Skin Solutions",
        "Barefaced Beauty Basics",
        "Pure Skin Perfection",
        "Skin Clarity Simplified",
        "Easy Elegance Skincare",
        "Flawless Skin Favorites",
        "Simplified Skincare Heroes",
        "The Purity Principle",
        "Bare Beauty Staples",
    ],
    "Makeup": [
        "Makeup Marvels",
        "Beauty Bests of the Year",
        "Glamour Goldlist",
        "Pinnacle of Palettes",
        "Elite Makeup Edit",
        "Cosmetics Connoisseurs",
        "Makeup Mastery Selection",
        "Beauty Game Changers",
        "The Makeup Elite",
        "2023 Beauty Icons",
    ],
    "Outfits": [
        "Wardrobe Revolution Essentials",
        "Chic Closet Must-Haves",
        "Style Elevation Staples",
        "Fashion Forward Finds",
        "Trendsetting Attire Picks",
        "Closet Upgrade Classics",
        "Essential Style Icons",
        "Outfit Enhancers",
        "Wardrobe Winners",
        "Clothing Game Changers",
    ],
}


background_image_path = (
    f"src/assets/data/{project_name}/blog/images/product_template.png"
)
output_file = f"src/assets/data/{project_name}/blog/images/"


GOOGLE_BLOGGER_API_KEY


import time

start_time = time.time()

total = 10
for category in list(title_mapping.keys()):
    print(category)
    # Generate and save  infographics
    for i in range(1, total):
        product_path = f"src/assets/data/{project_name}/blog/images/products/{category}"
        # rename them to png
        # rename_file_type(product_path)

        # create directory
        os.makedirs(f"{output_file}content/{category}", exist_ok=True)
        # convert
        title = random.sample(title_mapping[category], 1)[0].upper()
        infographic = create_product_grid(
            background_image_path,
            product_path,
            title=title,
        )
        infographic.save(f"{output_file}content/{category}/infographic_{i:02d}.png")


end_time = time.time()
print(f"Execution time: {end_time-start_time} seconds")
