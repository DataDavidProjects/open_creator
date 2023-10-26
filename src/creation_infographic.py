from typing import Tuple
from PIL import Image, ImageDraw, ImageFont
from processing.image_processing import image_effects
from processing.text_processing import caption_effects
import functools
import yaml
from processing.text_processing import get_coords
from config.config_utils import load_config


major_config = load_config("src/config/config.yaml")
project = major_config["project"]
minor_config = load_config(f"src/config/{project}/config.yaml")
params = {**major_config, **minor_config}

align = params["font"]["text_coords"]["align"]


def create_captioned_image(
    caption: str,
    font_path: str,
    img_path: str,
    save_to: str,
    text_color: str = "#0000",
    font_size: int = 30,
    wrap_block: int = 40,
    text_coords: Tuple[float, float] = (216.0, 453.6),
    align: str = align,
) -> None:
    """
    Create a captioned image.

    Parameters:
    - caption (str): The caption to add to the image.
    - font_path (str): The path to the font file.
    - img_path (str): The path to the image file.
    - save_to (str): The path to save the captioned image.
    - text_color (str): The color of the text. Default is "#0000".
    - font_size (int): The size of the font. Default is 30.
    - wrap_block (int): The maximum width of the text block. Default is 40.
    - text_coords (Tuple[float, float]): The x and y coordinates for the start of the text. Default is (216.0, 453.6).
    - effects (str) : effects filter on image.

    Returns:
    - image
    """
    font = ImageFont.truetype(font_path, font_size)
    raw_image = Image.open(img_path)

    image = image_effects(raw_image, effect="portrait")
    image = image_effects(image, effect="overlay")

    draw = ImageDraw.Draw(image)

    caption_blocks = caption_effects(
        caption=caption, effect=align, wrap_block=wrap_block
    )

    # Get the coordinates for the text
    if params["font"]["text_coords"]["auto"]:
        text_coords = get_coords(image, wrap_block, caption_blocks, font)
    else:
        text_coords = (
            params["font"]["text_coords"]["width"],
            params["font"]["text_coords"]["height"],
        )

    draw.text(
        text_coords,
        "\n".join(caption_blocks),
        font=font,
        fill=text_color,
        align=align,
    )

    if save_to:
        image.save(save_to)

    return image
