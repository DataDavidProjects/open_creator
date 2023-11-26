import os
import random
import sys
import uuid

import pandas as pd

sys.path.append(".")

from product_operations import ProductsInfographic, create_grid_positions

from scripts.infographics.product_operations import image_collect

PROJECT_NAME = "theallurecode"

for _ in range(5):
    # Sample a random title for each product card
    titles = [
        "Christmas Gifts Every Girl will Love",
        "The Ultimate Christmas Shopping for Girls",
        "Items you need to glow up before new year",
        "Christmas Gifts Your Girlies will Love",
        "Amazing Christmas Gift Ideas for Moms",
    ]

    # Constants for the layout
    DEFAULT_FONT_PATH = "C:/Users/david/Desktop/Projects/Dev/projects/open_creator/src/assets/fonts/Montserrat_700.ttf"
    title_font_path = "C:/Users/david/Desktop/Projects/Dev/projects/open_creator/src/assets/fonts/FLOWRISE.ttf"
    header_font_path = "C:/Users/david/Desktop/Projects/Dev/projects/open_creator/src/assets/fonts/FLOWRISE.ttf"
    desc_font_path = "arial.ttf"
    title_font_size = 50
    header_font_size = title_font_size / (1.68 * 1)
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
    categories = ["Makeup"]

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
    selected_products_df["image"] = selected_products_df["path"].str.extract(
        r"([^/]+$)"
    )
    selected_products_df["category"] = (
        selected_products_df["path"].str.split("/").str[7]
    )

    table_path = os.path.join(
        project_path, "products", "The Allure Code Product table.xlsx"
    )
    products_table = pd.read_excel(table_path).astype(str)
    products_table.columns = ["name", "category", "link", "image"]
    products_table["image"] += ".png"
    data = selected_products_df.merge(
        products_table, how="inner", on=["image", "category"]
    )

    # Initialize the infographic
    infographic = ProductsInfographic().create_canvas(
        canvas_width, canvas_height, "#ffffff"
    )

    # Add header section
    infographic.add_header(
        header_height,
        "#ffffff",
        text=random.sample(titles, 1)[0],
        title_font_path=title_font_path,
        title_font_size=title_font_size,
        text_color="#000000",
    )

    # Add footer section
    infographic.add_footer(
        footer_height,
        "#ffffff",
        text="Gift guides | www.benable.thealllurecode.com".upper(),
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

    # Add product cards with text and images from the data
    for n, ((top_left, bottom_right), row) in enumerate(
        zip(product_card_positions, data.itertuples(index=False))
    ):
        header = "MUST HAVE" if n == 4 else ""
        #    random.choices(population=["", "MUST HAVE"], weights=[0.8, 0.2], k=1)[0],
        product_image = row.file  # Extract the PIL Image object

        infographic.add_product_card(
            top_left,
            bottom_right,
            header,  # row.category,
            product_image,
            f"{n+1}.{row.name}",
            header_font_path,
            desc_font_path,
            int(header_font_size),
            int(desc_font_size),
        )
    # Generate a unique ID
    unique_id = uuid.uuid4().hex[:5]
    save = f"src/assets/data/{PROJECT_NAME}/pinterest/images/content_{unique_id}.png"
    # Display the layout
    if data.shape[0] == 9:
        infographic.canvas.save(save)
    else:
        print("PROBLEM")
        print(data[["path"]].tail().values)
        # infographic.canvas.show()
