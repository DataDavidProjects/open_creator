import random
import sys
import uuid

import pandas as pd

sys.path.append(".")

from scripts.infographics.product_operations import create_mix, create_product_grid
from src.utils.blogger_utils import create_blog_post, read_html_file, render_blog_post
from src.utils.firebase_utils import get_image_firebase, upload_firebase_storage

project_name = "theallurecode"
project_path = f"src/assets/data/{project_name}/blog"
unique_id = uuid.uuid4()


# Products for infographics
selected_products = create_mix(
    ["Skincare", "Fragrance", "Makeup"],
    f"src/assets/data/{project_name}/blog/images/",
    destination_folder="products",
)
# Create infographic
title_mapping = {
    "Mix_Skincare_Fragrance_Makeup": [
        "Christmas Gifts Every Girl will Love in 2023",
        "The Ultimate Christmas Shopping List for Girls 2023",
        "Items you need to glow up before 2024",
        "Makeup and Skincare that are actually worth your money",
        "Christmas Gifts Your Girlies will Love",
        "Amazing Christmas Gift Ideas for Mom 2023",
    ],
}

category = "Mix_Skincare_Fragrance_Makeup"
background_image_path = (
    f"src/assets/data/{project_name}/blog/images/product_template.png"
)
product_path = f"src/assets/data/{project_name}/blog/images/products/{category}"
title = random.sample(title_mapping[category], 1)[0]
infographic = create_product_grid(
    background_image_path,
    product_path,
    title=title.upper(),
)

i = unique_id[:3]
# save infographic generated
file_name = f"src/assets/data/{project_name}/blog/images/content/infographics/infographic_{i:02d}.png"
infographic.save(file_name)
# Upload infographic to Firebase
cloud_file = f"infographic_{i:02d}.png"
upload_firebase_storage(
    local_file=file_name,
    cloud_file=f"Blog/{project_name}/{cloud_file}",
)


# Benable data related to selected_products:List=[tuple(str)]
data = {
    "product": [
        "Product",
        "Product",
        "Product",
        "Product",
        "Product",
        "Product",
        "Product",
        "Product",
        "Product",
    ],
    "link": [
        "http://benable.com/product1",
        "http://benable.com/product2",
        "http://benable.com/product3",
        "http://benable.com/product4",
        "http://benable.com/product5",
        "http://benable.com/product6",
        "http://benable.com/product7",
        "http://benable.com/product8",
        "http://benable.com/product9",
    ],
    "description": [
        "Product",
        "Product",
        "Product",
        "Product",
        "Product",
        "Product",
        "Product",
        "Product",
        "Product",
    ],
    "image_name": selected_products,
}
df = pd.DataFrame(data)

# Create Blog
template_file_path = f"src/assets/data/{project_name}/blog/templates/blog_template.html"
output_file_path = f"{project_path}/tables/blog_{unique_id}.html"


introduction = "Discover the latest trends"
products = [
    {"name": row["product"], "href": row["link"]} for index, row in df.iterrows()
]

blog_content = {
    "introduction": introduction,
    "image_url": get_image_firebase(
        folder_path=f"Blog/{project_name}", image_name=cloud_file
    ),
    "products": products,
}

# Render Blog HTML File
render_blog_post(
    blog_content=blog_content,
    template_file_path=template_file_path,
    output_file_path=output_file_path,
)


# Post Blog

TOKEN_JSON_FILE = "scripts/token.json"
GOOGLE_BLOGSPOT_ID = 4309253655499790374

html_file_path = output_file_path
content = read_html_file(html_file_path)


response = create_blog_post(
    GOOGLE_BLOGSPOT_ID,
    title.title(),
    content,
    token_json_file=TOKEN_JSON_FILE,
)
print(response.json())  # To print the response from the API
