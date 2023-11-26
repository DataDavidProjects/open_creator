import os
import sys

import pandas as pd

sys.path.append(".")

from product_operations import ProductsInfographic, create_grid_positions

from scripts.infographics.product_operations import image_collect

PROJECT_NAME = "theallurecode"


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

# Sample a random title for each product card
titles = [
    "Christmas Gifts Every Girl will Love in 2023",
    "The Ultimate Christmas Shopping List for Girls 2023",
    "Items you need to glow up before new year",
    "Makeup and Skincare that are actually worth your money",
    "Christmas Gifts Your Girlies will Love",
    "Amazing Christmas Gift Ideas for Mom 2023",
]


# Constants for the layout
DEFAULT_FONT_PATH = "C:/Users/david/Desktop/Projects/Dev/projects/open_creator/src/assets/fonts/Montserrat_700.ttf"
title_font_path = "C:/Users/david/Desktop/Projects/Dev/projects/open_creator/src/assets/fonts/FLOWRISE.ttf"
header_font_path = "C:/Users/david/Desktop/Projects/Dev/projects/open_creator/src/assets/fonts/FLOWRISE.ttf"
desc_font_path = "arial.ttf"
title_font_size = 64
header_font_size = title_font_size / (1.68 * 1.2)
desc_font_size = header_font_size / (1.68 * 1.2)
margin = 50  # Margin between cards
num_columns = 3  # Adjusted for 3x3 grid
num_rows = 3  # Adjusted for 3x3 grid
canvas_width = 1200
canvas_height = 1800
header_height = int(canvas_height * 0.1)
footer_height = header_height


# Construct the path to the project's blog data
project_path = os.path.join("src", "assets", "data", PROJECT_NAME, "blog")
# Categories from which to collect product images
categories = ["Skincare", "Fragrance", "Makeup"]


# Collecting product images for the infographic
# This calls a function that randomly selects images from the given categories
selected_products = image_collect(
    subdir=categories,
    root=os.path.join(project_path, "images", "products"),
    n=num_columns * num_rows,
)
# Creating a DataFrame from the selected products for easier data manipulation
selected_products_df = pd.DataFrame(selected_products, columns=["file", "path"])
# Extracting image names and categories from the file paths for later use
selected_products_df["image"] = selected_products_df["path"].str.extract(r"([^/]+$)")
selected_products_df["category"] = selected_products_df["path"].str.split("/").str[7]

table_path = os.path.join(
    project_path, "products", "The Allure Code Product table.xlsx"
)
products_table = pd.read_excel(table_path).astype(str)
products_table.columns = ["name", "category", "link", "image"]
products_table["image"] += ".png"
data = selected_products_df.merge(products_table, how="inner", on=["image", "category"])


print(data.head())


# Initialize the infographic
infographic = ProductsInfographic().create_canvas(
    canvas_width, canvas_height, "#ffffff"
)

# Add header section
infographic.add_header(
    header_height,
    "#ffffff",
    text="Christmas Gifts Every Girl Love",
    title_font_path=title_font_path,
    title_font_size=title_font_size,
    text_color="#000000",
)

# Add footer section
infographic.add_footer(
    footer_height,
    "#ffffff",
    text="  Gift guides     |    www.benable.thealllurecode.com".upper(),
    title_font_path=desc_font_path,
    title_font_size=header_font_size / 1.68,
    text_color="black",
)


vertical_margin = 50
# Calculate product card positions
product_card_positions = create_grid_positions(
    canvas_width,
    canvas_height,
    num_columns,
    num_rows,
    header_height,
    footer_height,
    margin,
    vertical_margin,
)
print(product_card_positions)

# Add product cards with text and images from the data
for n, ((top_left, bottom_right), row) in enumerate(
    zip(product_card_positions, data.itertuples(index=False))
):
    product_image = row.file  # Extract the PIL Image object

    infographic.add_product_card(
        top_left,
        bottom_right,
        row.category,
        product_image,
        f"{n+1}.{row.name}",
        header_font_path,
        desc_font_path,
        int(header_font_size),
        int(desc_font_size),
    )

# Display the layout
infographic.canvas.show()
