import os
import random
import sys
import time
import uuid

import pandas as pd
import schedule

# Make sure the paths for custom modules are accessible
sys.path.append(".")

# Importing functions from other parts of the project
from scripts.infographics.product_operations import (
    create_grid_infographic,
    image_collect,
)
from src.utils.blogger_utils import create_blog_post, read_html_file, render_blog_post
from src.utils.firebase_utils import get_image_firebase, upload_firebase_storage

# for image name and scheduler
run_counter = 2


def blogger_job():
    global run_counter

    # Define project specific configurations
    project_name = "theallurecode"
    # Construct the path to the project's blog data
    project_path = os.path.join("src", "assets", "data", project_name, "blog")
    # Categories from which to collect product images
    categories = ["Skincare", "Fragrance", "Makeup"]

    # Define a unique identifier for this particular run
    unique_id = uuid.uuid4()

    # Collecting product images for the infographic
    # This calls a function that randomly selects images from the given categories
    selected_products = image_collect(
        subdir=categories, root=os.path.join(project_path, "images", "products"), n=9
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

    # Saving the generated infographic to the filesystem
    file_name = os.path.join(
        project_path,
        "images",
        "content",
        "infographics",
        f"infographic_{run_counter:02d}.png",
    )
    infographic.save(file_name)

    # Uploading the infographic to Firebase for online access
    cloud_file = f"infographic_{run_counter:02d}.png"
    upload_firebase_storage(
        local_file=file_name,
        cloud_file=f"Blog/{project_name}/blogger/{cloud_file}",
    )

    # Preparing data for the blog post
    table_path = os.path.join(
        project_path, "products", "The Allure Code Product table.xlsx"
    )
    products_table = pd.read_excel(table_path).astype(str)
    products_table.columns = ["name", "category", "link", "image"]
    products_table["image"] += ".png"
    data = selected_products_df.merge(
        products_table, how="inner", on=["image", "category"]
    )

    # Assembling the content for the blog post
    template_file_path = os.path.join(project_path, "templates", "blog_template.html")
    output_file_path = os.path.join(project_path, "tables", f"blog_{unique_id}.html")
    introduction = "Discover the latest trends"
    products = [
        {"name": row["name"], "href": row["link"]} for _, row in data.iterrows()
    ]
    blog_content = {
        "introduction": introduction,
        "image_url": get_image_firebase(
            folder_path=f"Blog/{project_name}/blogger",
            image_name=cloud_file,
        ),
        "products": products,
    }
    render_blog_post(
        blog_content=blog_content,
        template_file_path=template_file_path,
        output_file_path=output_file_path,
    )

    # Posting the blog to the blogging platform
    TOKEN_JSON_FILE = "scripts/token.json"
    GOOGLE_BLOGSPOT_ID = 4309253655499790374
    content = read_html_file(output_file_path)
    response = create_blog_post(
        GOOGLE_BLOGSPOT_ID,
        title.title(),
        content,
        token_json_file=TOKEN_JSON_FILE,
    )

    # Printing out the product data and the response from the blog post for debugging
    print(data[["image", "name"]])
    print(response.json())

    # Increment counter at success
    run_counter += 1


# Schedule the job every 10 seconds
schedule.every(10).seconds.do(blogger_job)

while True:
    schedule.run_pending()
    time.sleep(1)
