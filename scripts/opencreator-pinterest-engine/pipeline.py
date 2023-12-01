import os
import random
import sys
import uuid

import pandas as pd

sys.path.append(".")
from PIL import Image, ImageFont

from src.processing.product_processing import Infographic, image_collect
from src.utils.authentication import load_config
from src.utils.blogger_utils import create_blog_post, read_html_file, render_blog_post
from src.utils.firebase_utils import get_image_firebase, upload_firebase_storage
from src.utils.pinterest_utils import create_pinterest_pin

######################### Project metadata #####################################
PROJECT_NAME = "theallurecode"
PROJECT_PATH = os.path.join("src", "assets", "data", PROJECT_NAME, "blog")
config = load_config(project_name=PROJECT_NAME)
UNIQUE_ID = uuid.uuid4().hex[:5]
FILE_NAME = f"src/assets/data/{PROJECT_NAME}/pinterest/images/content_{UNIQUE_ID}.png"
################################################################################


# ___________________________ Content  _________________________________________#


# SELECT PRODUCTS
N_PRODUCTS = 9
# TODO conversion to cloud

TABLE = "The Allure Code Product table.xlsx"
PRODUCT_TABLE = os.path.join(PROJECT_PATH, "products", TABLE)
# Read Product table drop nan
products_table = pd.read_excel(PRODUCT_TABLE).dropna().astype(str)

# Define columns
products_table.columns = ["full-name", "name", "category", "link", "image"]
products_table["image"] += ".png"

# Define category of products
categories = ["Makeup", "Fragrance"]

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


# CREATE INFOGRAPHIC


def create_placeholder_image(size, color):
    """Create a simple placeholder image"""
    img = Image.new("RGB", size, color)
    return img


# Placeholder image creation
PLACEHOLDER_IMAGE_SIZE = (240, 255)
PLACEHOLDER_IMAGE_COLOR = "#000000"
placeholder_image = create_placeholder_image(
    PLACEHOLDER_IMAGE_SIZE, PLACEHOLDER_IMAGE_COLOR
)


cover_path = "C:/Users/david/Desktop/Projects/Dev/projects/open_creator/scripts/opencreator-pinterest-engine/template.png"

COVER_IMAGE = Image.open(cover_path)
# Define Canvas
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 1500
BACKGROUND_INFOGRAPHIC = "#E7E7E7"
PRODUCT_BACKGROUND_COLOR = "#EFEFEF"
PRODUCT_CARD_BACKGROUND = "#FFFFFF"

# Constants for layout proportions
MARGIN_HORIZONTAL = 60
MARGIN_TOP = 202
MARGIN_BOTTOM = 180
GRID_HORIZONTAL_SPACING = 50
GRID_VERTICAL_SPACING = 70
CARD_WIDTH = 260
CARD_HEIGHT = 320
CORNER_RADIUS = 20


# Fonts (using default font as a placeholder)

TITLE_FONT_PATH = "C:/Users/david/Desktop/Projects/Dev/projects/open_creator/src/assets/fonts/FLOWRISE.ttf"
PRODUCT_DESC_FONT_PATH = "C:/Users/david/Desktop/Projects/Dev/projects/open_creator/src/assets/fonts/ArialBold.ttf"

TITLE_FONT_SIZE = 80
HEADER_FONT_SIZE = TITLE_FONT_SIZE / (1.68 * 1.0)
DESC_FONT_SIZE = HEADER_FONT_SIZE / (1.68 * 2)
FOOTER_FONT_SIZE = HEADER_FONT_SIZE / 1.68

TITLE_TEXT = random.sample(
    [
        "Hot Right Now",
        "Girl's Favorites",
        "2024 Beauty Trends",
        "Girl's Must-Haves",
        "Easy Beauty Hacks",
        "Simple Glam Picks",
        "Daily Beauty Tools",
        "Affordable Finds",
        "Style on Budget",
        "Chic & Simple",
        "Everyday Essentials",
        "Quick Fixes",
        "Top Beauty Picks",
        "Smart Beauty Buys",
        "Fresh Look Ideas",
        "Trendy & Easy",
        "Beauty Shortcuts",
        "Cute Accessories",
    ],
    1,
)[0]
TITLE_FONT = ImageFont.truetype(TITLE_FONT_PATH, TITLE_FONT_SIZE)
PRODUCT_TEXT_COLOR = "#FFFFFF"
PRODUCT_DESC_FONT = ImageFont.truetype(
    PRODUCT_DESC_FONT_PATH,
    DESC_FONT_SIZE,
)
# Calculate vertical positions of the rows
row_positions = [
    MARGIN_TOP + i * (CARD_HEIGHT + GRID_VERTICAL_SPACING) for i in range(3)
]

# Calculate horizontal positions of the columns
col_positions = [
    MARGIN_HORIZONTAL + i * (CARD_WIDTH + GRID_HORIZONTAL_SPACING) for i in range(3)
]

TITLE_POSITION = (20, 110)
# Constants for the text box
TEXT_BOX_COLOR = "#A29888"  # Color for the text background
TEXT_BOX_HEIGHT = 45  # Height of the text background box
TEXT_BOX_WIDTH = 200
TEXT_BOX_MARGIN_BOTTOM = 20
# Create canvas
infographic = (
    Infographic()
    .create_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, BACKGROUND_INFOGRAPHIC)
    # add cover image
    .add_image(COVER_IMAGE, (0, 0))
    .add_text(
        TITLE_TEXT, TITLE_POSITION, TITLE_FONT, "#000000", 1000, alignment="center"
    )
)

# Add product sections with rounded corners
for row in range(3):
    for col in range(3):
        # Create bounding box for product card
        card_top_left = (col_positions[col], row_positions[row])
        card_bottom_right = (
            card_top_left[0] + CARD_WIDTH,
            card_top_left[1] + CARD_HEIGHT,
        )
        infographic.create_section(
            [card_top_left, card_bottom_right],
            PRODUCT_CARD_BACKGROUND,
            corners=CORNER_RADIUS,
            line_width=3,
            line_color="#A29888",
        )

        # Add placeholder image
        image_top_left = (
            card_top_left[0] + (CARD_WIDTH - PLACEHOLDER_IMAGE_SIZE[0]) // 2,
            card_top_left[1] + 20,
        )

        # iterate over data at position n column 0 to get image
        placeholder_image = data.iloc[row * 3 + col, 0]
        infographic.add_image(placeholder_image, image_top_left)

        text_bg_x_center = (card_top_left[0] + card_bottom_right[0]) // 2
        text_bg_bottom_y = card_bottom_right[1] + TEXT_BOX_MARGIN_BOTTOM
        text_bg_top_left = (
            text_bg_x_center - TEXT_BOX_WIDTH // 2,
            text_bg_bottom_y - TEXT_BOX_HEIGHT,
        )
        text_bg_bottom_right = (
            text_bg_x_center + TEXT_BOX_WIDTH // 2,
            text_bg_bottom_y,
        )
        infographic.create_section(
            [text_bg_top_left, text_bg_bottom_right], TEXT_BOX_COLOR
        )

        # Calculate the position for the text, assuming a single line of text
        product_text = data.iloc[row * 3 + col, 5].upper()
        text_size = PRODUCT_DESC_FONT.getbbox(
            product_text
        )  # Get the bounding box of the text
        text_width = text_size[2] - text_size[0]
        text_x = (
            card_top_left[0] + (CARD_WIDTH - text_width) // 2
        )  # Center the text horizontally
        text_y = (
            text_bg_top_left[1] + (TEXT_BOX_HEIGHT - (text_size[3] - text_size[1])) // 2
        )  # Vertically center in the text box
        infographic.add_text(
            product_text, (text_x, text_y), PRODUCT_DESC_FONT, PRODUCT_TEXT_COLOR, 500
        )

# Show the canvas
infographic.canvas.show()


# Display the layout
if data.shape[0] == N_PRODUCTS:
    infographic.canvas.save(FILE_NAME)
# ______________________________________________________________________________#


############################# Firebase #########################################

# Uploading the infographic to Firebase
CLOUD_FILE = f"infographic_{UNIQUE_ID}.png"
upload_firebase_storage(
    local_file=FILE_NAME,
    cloud_file=f"Blog/{PROJECT_NAME}/pinterest/{CLOUD_FILE}",
)

# Fetch image from firebase
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
BLOG_TITLE = TITLE_TEXT

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
PIN_TITLE = TITLE_TEXT
PIN_IMAGE_URL = firebase_image
PIN_DESCRIPTION = ""  #
PIN_LINK = BLOG_URL


# Post pinterest
pin_response = create_pinterest_pin(
    USER_TOKEN, BOARD_ID, PIN_TITLE, PIN_LINK, PIN_IMAGE_URL, PIN_DESCRIPTION
)
################################################################################
