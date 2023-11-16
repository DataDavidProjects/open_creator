import os
import random
import sys

sys.path.append(".")

from product_operations import create_product_grid

project_name = "theallurecode"


title_mapping = {
    "Fragrance": [
        "Scents That will Make You Irresistible",
        "Fragrances that Make The Perfect Gift for Every Girl",
        "Fragrances You can Blind Buy 2023",
        "How to Smell Irresistible:  Fool proof fragrances",
        "Fragrances You Need to Try in 2023",
    ],
    "Skincare": [
        "Skincare Items You Need to Clear Your Skin",
        "These  Products will Clear Your Skin",
        "How to get the best skin of your life: Your No Bullsh*t Guide",
        "Christmas Gift Ideas for Your Skincare Girlies",
        "Skincare Products that are actually worth your money",
    ],
    "Makeup": [
        "The best makeup products of 2023",
        "Must Have Makeup:  Items You Cannot Mix",
        "Tutorial: How To Get the Victoria’s Secret Makeup look",
        "Christmas Wishlist 2023: Makeup Edition",
        "What to get for Christmas to your makeup obsessed besties",
    ],
    "Mix_Skincare_Fragrance_Makeup": [
        "Christmas Gifts Every Girl will Love in 2023",
        "The Ultimate Christmas Shopping List for Girls 2023",
        "Items you need to glow up before 2024",
        "Makeup and Skincare that are actually worth your money",
        "Christmas Gift Ideas for the Women in Your Life",
        "Christmas Gifts Your Girlies will Love",
        "Amazing Christmas Gift Ideas for Mom 2023",
    ],
}


background_image_path = (
    f"src/assets/data/{project_name}/blog/images/product_template.png"
)
output_file = f"src/assets/data/{project_name}/blog/images/"


import time

start_time = time.time()

# Create for each category n infographics
total = 50
for category in list(title_mapping.keys()):
    print(category)
    # Generate and save  infographics
    for i in range(1, total):
        # create the path
        product_path = f"src/assets/data/{project_name}/blog/images/products/{category}"
        # rename them to png
        # rename_file_type(product_path)

        # create directory
        os.makedirs(f"{output_file}content/{category}", exist_ok=True)
        # generate title based on dictionary
        title = random.sample(title_mapping[category], 1)[0].upper()
        # make infographic
        infographic = create_product_grid(
            background_image_path,
            product_path,
            title=title,
        )
        infographic.save(f"{output_file}content/{category}/infographic_{i:02d}.png")


end_time = time.time()
print(f"Execution time: {end_time-start_time} seconds")


# create_mix(["Skincare", "Fragrance", "Makeup"], output_file, n=9)
