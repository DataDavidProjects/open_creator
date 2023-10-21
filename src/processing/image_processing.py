from PIL import Image
from typing import Callable, Dict, Tuple
from PIL import Image, ImageFilter, ImageFont, ImageDraw
import functools
import yaml
import os
import random
from typing import List


# Load parameters from YAML file
with open("config.yaml", "r") as file:
    params = yaml.safe_load(file)


def get_random_image_path(directory: str) -> str:
    """
    Get a random image path from a specified directory.

    Parameters:
        - directory (str): The directory to get the random image from.

    Returns:
        - str: The path to a randomly selected image.
    """
    files = [
        f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))
    ]
    return os.path.join(directory, random.choice(files))


def read_image(image_path: str) -> Image:
    """
    Reads an image from the specified path using the Pillow library.

    Parameters:
    - image_path (str): The path of the image file to be read.

    Returns:
    - Image object: The image loaded into memory.
    """
    img = Image.open(image_path)
    return img


def apply_overlay(
    image: Image.Image, color: str = "#0000", alpha: float = 0.5
) -> Image.Image:
    """
    Apply a colored transparent overlay to an image.

    Parameters:
        - image (Image.Image): The original image.
        - color (str, optional): The color of the overlay. Defaults to black "#0000".
        - alpha (float, optional): The transparency of the overlay, between 0 (completely transparent) and 1 (completely opaque). Defaults to 0.5.

    Returns:
        - Image.Image: The image with the overlay applied.
    """
    # Ensure the alpha value is within the valid range
    alpha = max(0, min(alpha, 1))

    # Create a new image with the specified color and the same size and mode as the original image
    overlay = Image.new("RGBA", image.size, color)

    # Ensure the original image is in 'RGBA' mode so it has an alpha channel
    image = image.convert("RGBA")

    # Blend the original image and the overlay using the specified alpha value
    blended_image = Image.blend(image, overlay, alpha)

    return blended_image


def apply_blur(image: Image) -> Image:
    """Applies a blur effect to the image.

    Args:
        image (Image): The image to blur.

    Returns:
        Image: The blurred image.
    """
    return image.filter(ImageFilter.BLUR)


def apply_portrait(
    img: Image.Image, color: str = "#FFFFFF", margin: float = 0.95
) -> Image.Image:
    """
    Applies a portrait effect by drawing a rectangle-like shape on the image.

    Parameters:
    - img (Image.Image): The image to apply the effect to.
    - color (str): The color of the lines.
    - margin (float, optional): The margin as a percentage of the image dimensions. Defaults to 0.95.

    Returns:
    - Image.Image: The image with the portrait effect applied.
    """
    # Get image size
    width, height = img.size

    # Calculate dimensions as per margin
    x_margin = width * margin
    y_margin = height * margin

    # Coordinates for lines
    top_left = (x_margin, y_margin)
    top_right = (width - x_margin, y_margin)
    bottom_left = (x_margin, height - y_margin)
    bottom_right = (width - x_margin, height - y_margin)

    # Draw lines with color
    draw = ImageDraw.Draw(img)
    draw.line([top_left, top_right], fill=color)
    draw.line([top_right, bottom_right], fill=color)
    draw.line([bottom_right, bottom_left], fill=color)
    draw.line([bottom_left, top_left], fill=color)

    return img


alpha = params["image_processing"]["alpha_overlay"]
color_overlay = params["image_processing"]["color_overlay"]
color_portait = params["image_processing"]["color_portait"]

image_effect_dict = {
    "portrait": functools.partial(apply_portrait, color=color_portait),
    "overlay": functools.partial(apply_overlay, color=color_overlay, alpha=alpha),
    "blur": functools.partial(apply_blur, None),
}


def image_effects(
    image: Image,
    effect: str = None,
    effect_dict: Dict[str, Callable] = image_effect_dict,
) -> Image:
    """Applies the specified effect to the image.

    Args:
        image (Image): The image to apply the effect to.
        effect (str, optional): The name of the effect to apply. Defaults to None.
        effect_dict (Dict[str, Callable], optional): A dictionary mapping effect names to functions. Defaults to None.


    Returns:
        Image: The modified image, or the original image if no valid effect was specified.
    """
    if effect in effect_dict:
        image = effect_dict[effect](image)

    return image
