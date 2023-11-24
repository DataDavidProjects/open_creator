import os
import random
import sys
import uuid

import pandas as pd

# Make sure the paths for custom modules are accessible
sys.path.append(".")

# Importing functions from other parts of the project
from scripts.infographics.product_operations import (
    create_grid_infographic,
    image_collect,
)

# Define project specific configurations
project_name = "theallurecode"
# Construct the path to the project's blog data
project_path = os.path.join("src", "assets", "data", project_name, "blog")
# Categories from which to collect product images
categories = ["Skincare", "Fragrance", "Makeup"]

# Define a unique identifier for this particular run
unique_id = uuid.uuid4()
print(f"{unique_id.hex[:5]} ")
# Collecting product images for the infographic
# This calls a function that randomly selects images from the given categories
selected_products = image_collect(
    subdir=categories, root=os.path.join(project_path, "images", "products"), n=9
)
# Creating a DataFrame from the selected products for easier data manipulation
selected_products_df = pd.DataFrame(selected_products, columns=["file", "path"])
# Extracting image names and categories from the file paths for later use
selected_products_df["image"] = selected_products_df["path"].str.extract(r"([^/]+$)")
selected_products_df["category"] = selected_products_df["path"].str.split("/").str[7]

# Generating an infographic from the collected product images
# Titles for the infographic are chosen randomly from a predefined list
category = "Mix" + "_".join(categories)
title_mapping = {
    category: [
        "Christmas Gifts Every Girl will Love in 2023",
        "The Ultimate Christmas Shopping List for Girls 2023",
        "Items you need to glow up before 2024",
        "Makeup and Skincare that are actually worth your money",
        "Christmas Gifts Your Girlies will Love",
        "Amazing Christmas Gift Ideas for Mom 2023",
    ],
}
title = random.choice(title_mapping[category])
background_image_path = os.path.join(project_path, "images", "product_template.png")
infographic = create_grid_infographic(
    background_path=background_image_path,
    images=selected_products_df["file"].tolist(),
    header_text=title.upper(),
)


infographic.show()
