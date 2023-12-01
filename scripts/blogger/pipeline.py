import os
import sys
import uuid

import pandas as pd

sys.path.append(".")
from src.processing.product_processing import (
    ProductsInfographic,
    create_grid_positions,
    image_collect,
)
from src.utils.authentication import load_config
from src.utils.blogger_utils import create_blog_post, read_html_file, render_blog_post
from src.utils.firebase_utils import get_image_firebase, upload_firebase_storage
from src.utils.pinterest_utils import create_pinterest_pin

# Project metadata
PROJECT_NAME = "theallurecode"
PROJECT_PATH = os.path.join("src", "assets", "data", PROJECT_NAME, "blog")
config = load_config(project_name=PROJECT_NAME)

###################   metadata infographic #####################################

# Define Canvas
CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 1800

# Define colors
BACKGROUND_INFOGRAPHIC = "#FFFFFF"
TEXT_COLOR = "#000000"

# Define measure layout
HEADER_HEIGHT = int(CANVAS_HEIGHT * 0.1)
FOOTER_HEIGHT = HEADER_HEIGHT

# TODO fix absolute import font fetch
root = "C:/Users/david/Desktop/Projects/Dev/projects"
# Font
DEFAULT_FONT_PATH = root + "/open_creator/src/assets/fonts/FLOWRISE.ttf"
TITLE_FONT_PATH = DEFAULT_FONT_PATH
HEADER_FONT_PATH = DEFAULT_FONT_PATH
DESC_FONT_PATH = "arial.ttf"

# Hierarchy font
TITLE_FONT_SIZE = 105
HEADER_FONT_SIZE = TITLE_FONT_SIZE / (1.68 * 2)
DESC_FONT_SIZE = HEADER_FONT_SIZE / (1.68 * 1.2)
FOOTER_FONT_SIZE = HEADER_FONT_SIZE / 1.68

# Grid Products
NUM_COLUMNS = 3
NUM_ROWS = 3
N_PRODUCTS = NUM_COLUMNS * NUM_ROWS

# Define title
TITLES = [
    "Christmas Gifts Every Girl will Love",
    "The Ultimate Christmas Shopping for Girls",
    "Items you need to glow up before new year",
    "Christmas Gifts Your Girlies will Love",
    "Amazing Christmas Gift Ideas for Moms",
]


# Define title
TITLE = "Christmas Gifts Ideas".upper()  # random.sample(TITLES, 1)[0].title()
# Define header
HEADER = "MUST HAVE".upper()
# Define footer
FOOTER_TEXT = "Gift guides | www.benable.theallurecode.com".upper()

################################################################################

############################ select products ###################################

# TODO conversion to cloud

TABLE = "The Allure Code Product table.xlsx"
PRODUCT_TABLE = os.path.join(PROJECT_PATH, "products", TABLE)
# Read Product table drop nan
products_table = pd.read_excel(PRODUCT_TABLE).dropna().astype(str)

# Define columns
products_table.columns = ["name", "category", "link", "image"]
products_table["image"] += ".png"

# Define category of products
categories = ["Makeup"]

selected_products = image_collect(
    subdir=categories,
    root=os.path.join(PROJECT_PATH, "images", "products"),
    n=N_PRODUCTS,
)
selected_products_df = pd.DataFrame(selected_products, columns=["file", "path"])
selected_products_df["image"] = selected_products_df["path"].str.extract(r"([^/]+$)")
selected_products_df["category"] = selected_products_df["path"].str.split("/").str[7]

# Refine names
PRODUCT_TABLE = products_table
IMAGE_TABLE = selected_products_df

# Create final table as Join products_table as PRODUCT_TABLE with selected_products_df as IMAGE_TABLE
data = selected_products_df.merge(products_table, how="inner", on=["image", "category"])
print(data)
################################################################################

############################## create infographic ##############################

# Create canvas
infographic = ProductsInfographic().create_canvas(
    CANVAS_WIDTH, CANVAS_HEIGHT, BACKGROUND_INFOGRAPHIC
)

HEADER_TEXT = TITLE
# Add header section
infographic.add_header(
    HEADER_HEIGHT,
    BACKGROUND_INFOGRAPHIC,
    text=HEADER_TEXT,
    title_font_path=TITLE_FONT_PATH,
    title_font_size=TITLE_FONT_SIZE,
    text_color=TEXT_COLOR,
)

# Add footer section
infographic.add_footer(
    FOOTER_HEIGHT,
    BACKGROUND_INFOGRAPHIC,
    text=FOOTER_TEXT,
    title_font_path=DESC_FONT_PATH,
    title_font_size=FOOTER_FONT_SIZE,
    text_color=TEXT_COLOR,
)

VERTICAL_MARGIN = 50
PRODUCT_MARGIN = 50
# Add product grid
product_card_positions = create_grid_positions(
    canvas_width=CANVAS_WIDTH,
    canvas_height=CANVAS_HEIGHT,
    num_columns=NUM_COLUMNS,
    num_rows=NUM_ROWS,
    header_height=HEADER_HEIGHT,
    footer_height=FOOTER_HEIGHT,
    margin=PRODUCT_MARGIN,
    vertical_margin=VERTICAL_MARGIN,
)

# Add product cards with text and images from the data
for n, ((top_left, bottom_right), row) in enumerate(
    zip(product_card_positions, data.itertuples(index=False))
):
    product_image = row.file  # Extract the PIL Image object

    infographic.add_product_card(
        top_left,
        bottom_right,
        HEADER if n == 4 else "",
        product_image,
        f"{n+1}. {row.name}",
        HEADER_FONT_PATH,
        DESC_FONT_PATH,
        int(HEADER_FONT_SIZE),
        int(DESC_FONT_SIZE),
    )

# Generate a unique ID
UNIQUE_ID = uuid.uuid4().hex[:5]
FILE_NAME = f"src/assets/data/{PROJECT_NAME}/pinterest/images/content_{UNIQUE_ID}.png"


infographic.canvas.show()
# Display the layout
if data.shape[0] == N_PRODUCTS:
    infographic.canvas.save(FILE_NAME)

################################################################################

############################# Firebase #########################################

# Uploading the infographic to Firebase for online access
CLOUD_FILE = f"infographic_{UNIQUE_ID}.png"
upload_firebase_storage(
    local_file=FILE_NAME,
    cloud_file=f"Blog/{PROJECT_NAME}/pinterest/{CLOUD_FILE}",
)

# Fetch image firebase
firebase_image = get_image_firebase(
    folder_path=f"Blog/{PROJECT_NAME}/pinterest",
    image_name=CLOUD_FILE,
)


assert firebase_image is not None
################################################################################


############################# Blog Post ########################################

# Define metadata BLOG
TOKEN_JSON_FILE = "scripts/token.json"
GOOGLE_BLOGSPOT_ID = 4309253655499790374


template_file_path = os.path.join(PROJECT_PATH, "templates", "blog_template.html")
output_file_path = os.path.join(PROJECT_PATH, "tables", f"blog_{UNIQUE_ID}.html")

BLOG_INTRODUCTION = "Click down on the list to shop my favourites!"
BLOG_TITLE = TITLE

# Assembling the content for the blog post
products = [{"name": row["name"], "href": row["link"]} for _, row in data.iterrows()]
blog_content = {
    "introduction": BLOG_INTRODUCTION,
    "image_url": firebase_image,
    "products": products,
}

# Render blog template and save
render_blog_post(
    blog_content=blog_content,
    template_file_path=template_file_path,
    output_file_path=output_file_path,
)

# Post blog
content = read_html_file(output_file_path)
# Get the Blog URL
BLOG_URL = create_blog_post(
    GOOGLE_BLOGSPOT_ID,
    BLOG_TITLE,
    content,
    token_json_file=TOKEN_JSON_FILE,
).get("url")


################################################################################


############################# Pinterest ########################################

# TODO Optimize metadata based on SEO keywords

# Generate metadata pin
USER_TOKEN = config["THEALLURECODE_PINTEREST_ACCESS_TOKEN"]
BOARD_ID = "875668789986577789"
PIN_TITLE = TITLE
PIN_IMAGE_URL = firebase_image

# Get Keywords
params = {"interests": ["beauty", "womens_fashion"], "limit": 10}
INTERESTS = ["beauty", "womens_fashion", "christmas_gifts"]
REGION = "us"
TREND_TYPE = "monthly"
# trends = get_trending_keywords(REGION, TREND_TYPE, params, USER_TOKEN)

PIN_DESCRIPTION = ""

PIN_LINK = BLOG_URL


# Post pinterest
pin_response = create_pinterest_pin(
    USER_TOKEN, BOARD_ID, PIN_TITLE, PIN_LINK, PIN_IMAGE_URL, PIN_DESCRIPTION
)

################################################################################
