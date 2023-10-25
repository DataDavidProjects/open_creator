from typing import Tuple, List
import textwrap
from typing import Callable, Dict, Tuple
import functools
import yaml
from PIL import Image, ImageDraw, ImageFont
from config.config_utils import load_config

major_config = load_config("config.yaml")
project = major_config["project"]
minor_config = load_config(f"src/config/{project}/config.yaml")
params = {**major_config, **minor_config}


def get_coords(
    img: Image.Image,
    wrap_block: int,
    caption_blocks: List[str],
    font: ImageFont.FreeTypeFont,
) -> Tuple[int, int]:
    img_width, img_height = img.size

    # Find the widest line of text
    draw = ImageDraw.Draw(img)
    text_width = max(
        [draw.textbbox((0, 0), line, font=font)[2] for line in caption_blocks]
    )

    # Calculate the total height of the text block
    text_height = len(caption_blocks) * (font.getmetrics()[1])

    # Calculate the coordinates to center the text
    x_coord = (img_width - text_width) // 2
    y_coord = (img_height - text_height - wrap_block) // 2

    return (x_coord, y_coord)


def apply_left(caption: str, wrap_block: int) -> List[str]:
    wrapper = textwrap.TextWrapper(width=wrap_block, expand_tabs=False)
    caption_blocks = wrapper.wrap(text=caption)
    return caption_blocks


def apply_right(caption: str, wrap_block: int) -> List[str]:
    wrapper = textwrap.TextWrapper(width=wrap_block, expand_tabs=False)
    caption_blocks = wrapper.wrap(text=caption)
    # Right-align each block by padding with spaces
    caption_blocks = [block.rjust(wrap_block) for block in caption_blocks]
    return caption_blocks


def apply_center(caption: str, wrap_block: int) -> List[str]:
    wrapper = textwrap.TextWrapper(width=wrap_block)
    caption_blocks = wrapper.wrap(text=caption)
    # Center-align each block by padding with spaces
    caption_blocks = [block.center(wrap_block) for block in caption_blocks]
    return caption_blocks


wrap_block = params["font"]["wrap_block"]
text_effect_dict = {
    "left": functools.partial(apply_left, wrap_block=wrap_block),
    "right": functools.partial(apply_right, wrap_block=wrap_block),
    "center": functools.partial(apply_center, wrap_block=wrap_block),
}


def caption_effects(
    caption: str,
    effect: str,
    wrap_block: int,
    effect_dict: Dict[str, Callable] = text_effect_dict,
) -> List[str]:
    """Handle a multiline string and create caption blocks

    Args:
        caption (str): original caption.
        effect (str): effect to apply
        wrap_block (int): width of each block

    Returns:
        List[str]: caption blocks
    """

    if effect in effect_dict:
        caption_blocks = effect_dict[effect](caption)

    return caption_blocks
