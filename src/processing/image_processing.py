from typing import Callable, Dict, Tuple, Union

from PIL import Image, ImageDraw, ImageFilter


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def reduce_size(img: Image.Image, size: Tuple[int, int]) -> Image.Image:
    """
    Reduces the size of an image to fit within a bounding box, while maintaining its aspect ratio.

    Parameters:
    - img (Image.Image): The original image to be resized.
    - max_size (Tuple[int, int]): The maximum size for the thumbnail (width, height).

    Returns:
    - Image.Image: The resized image.
    """
    # Create a copy of the original image to avoid modifying it
    resized_img = img.copy()

    # Resize the image using the thumbnail method
    resized_img.thumbnail(size)

    return resized_img


def apply_image(
    parent: Image.Image, child: Image.Image, paste_position: Union[Tuple[int, int], str]
) -> Image.Image:
    """
    Positions a child image onto a parent image at a specified position.

    Parameters:
    - parent (Image.Image): The parent image where the child image will be placed.
    - child (Image.Image): The child image to be placed onto the parent image.
    - paste_position (Tuple[int, int]| str): The position (x, y) where the child image should be placed on the parent image.

    Returns:
    - Image.Image: The resulting image after placing the child image onto the parent image.
    """
    # Create a copy of the parent image to avoid modifying the original image
    result_img = parent.copy()

    # Paste the child image onto the copy of the parent image at the specified position
    if paste_position == "center":
        width_parent, height_parent = parent.size
        width_child, height_child = child.size

        x = (width_parent - width_child) // 2
        y = (height_parent - height_child) // 2
        paste_position = (x, y)

    result_img.paste(child, paste_position)

    return result_img


def apply_padding(
    img: Image.Image,
    size: Tuple[int, int] = (1080, 1920),
    padding_color: str = "#000000",
) -> Image.Image:
    """
    Applies padding to an image to achieve a desired size.

    Parameters:
    - img (Image.Image): The original image to be padded.
    - size (Tuple[int, int]): The desired size of the image after padding (width, height).
        Default is (1080, 1920).
    - padding_color (str): The color of the padding as a hex color code. Default is '#000000' (black).

    Returns:
    - Image.Image: The padded image.
    """
    rgb_padding_color = hex_to_rgb(padding_color)

    # Create a new image with the desired size and padding color
    padded_img = Image.new("RGB", size, rgb_padding_color)

    # Calculate the position to paste the original image into the center of the new image
    paste_position = ((size[0] - img.width) // 2, (size[1] - img.height) // 2)

    # Paste the original image onto the new blank image
    padded_img.paste(img, paste_position)

    return padded_img


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


def image_effects(
    image: Image,
    effect: str = None,
    effect_dict: Dict[str, Callable] = {},
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
