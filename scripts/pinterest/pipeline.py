import sys

sys.path.append(".")
from src.utils.authentication import load_config
from src.utils.pinterest_utils import create_pinterest_pin

PROJECT_NAME = "theallurecode"

config = load_config(project_name=PROJECT_NAME)


USER_TOKEN = config["THEALLURECODE_PINTEREST_ACCESS_TOKEN"]


BOARD_ID = "875668789986577789"


title = "AMAZING CHRISTMAS GIFTS IDEAS FOR MOMS"
link = "https://benable.com/TheAllureCode/must-have-makeup-products"
image_url = ""
description = "Make up ideas."

pin_response = create_pinterest_pin(
    USER_TOKEN, BOARD_ID, title, link, image_url, description
)
print(pin_response)
