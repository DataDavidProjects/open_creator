import random
import sys

sys.path.append(".")
from src.processing.image_processing import (
    create_grid_infographic,
    fill_transparency,
    pad_image_to_size,
    reduce_size,
)
from src.utils.file_operations import read_images

# The actual usage of this function should be with real image paths and PIL images.

# Example usage of the function
background_image_path = "src/assets/data/theallurecode/blog/images/product_template.png"
product_path = "src/assets/data/theallurecode/blog/images/products/SkinCare"

# Read the images from the directory
original_products = read_images(path=product_path)

# Reduce and then pad the images to a size of 500x500
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
    header_text="BestSkinCare Routine".upper(),
    header_height=200,
)

# Display the infographic
infographic.show()
infographic.save("src/assets/data/theallurecode/blog/images/infographic.png")
