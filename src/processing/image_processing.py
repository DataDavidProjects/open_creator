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


from PIL import Image


def pad_image_to_size(img: Image.Image, target_size: Tuple[int, int]) -> Image.Image:
    """
    Adds padding to an image to make it match a specified size with a white background.

    Parameters:
    - img (Image.Image): The original image to be padded.
    - target_size (Tuple[int, int]): The target size (width, height) for the image after padding.

    Returns:
    - Image.Image: The padded image.
    """
    # Reduce the image size if it's larger than the target size, maintaining aspect ratio
    img.thumbnail(target_size)

    # Create a new image with a white background and the target size
    padded_img = Image.new("RGB", target_size, "white")

    # Calculate the position to paste the resized image onto the white background
    paste_x = (target_size[0] - img.width) // 2
    paste_y = (target_size[1] - img.height) // 2

    # Paste the resized image onto the white background
    padded_img.paste(img, (paste_x, paste_y))

    return padded_img


def fill_transparency(
    img: Image.Image, fill_color: Tuple[int, int, int] = (255, 255, 255)
) -> Image.Image:
    """
    Fills the transparent areas of an image with the given fill_color.

    Parameters:
    - img (Image.Image): The original image that may have transparency.
    - fill_color (Tuple[int, int, int]): The RGB color tuple to fill the background. Default is white.

    Returns:
    - Image.Image: The image with transparency filled.
    """
    # Check if the image has an alpha channel
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        # Ensure the image is in RGBA mode for processing
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        # Create a new image with a white background and the same size
        background = Image.new("RGB", img.size, fill_color)
        # Paste the image onto the background, using the alpha channel as the mask
        background.paste(
            img, mask=img.split()[3]
        )  # Split off the alpha channel and use it as a mask
        return background
    else:
        return img


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


from typing import List

from PIL import Image, ImageDraw, ImageFont


def create_grid_infographic(
    background_path: str,
    images: List[Image.Image],
    header_text: str,
    footer_text: str = None,
    font_path: str = "arial.ttf",
    font_size: int = 50,
    header_height: int = 150,
    footer_height: int = 150,
) -> Image.Image:
    """
    Creates an infographic with a header, a grid of images, and a footer.
    :param background_path: Path to the background image.
    :param images: List of PIL.Image objects to create the grid.
    :param header_text: Text to be placed in the header.
    :param footer_text: Optional text to be placed in the footer.
    :param font_path: Path to the font file to be used.
    :param font_size: Size of the font to be used for the header and footer text.
    :param header_height: Height of the header area.
    :param footer_height: Height of the footer area.
    :return: A PIL.Image object representing the completed infographic.
    """
    # Load the background image
    background_image = Image.open(background_path)

    # Get dimensions for the grid images
    grid_width = background_image.width // 3
    grid_height = (background_image.height - header_height - footer_height) // 3

    # Paste the grid images onto the background image
    for i, img in enumerate(images):
        x = (i % 3) * grid_width
        y = (i // 3) * grid_height + header_height
        background_image.paste(img.resize((grid_width, grid_height)), (x, y))

    # Create draw object for the background image
    draw = ImageDraw.Draw(background_image)

    # Load font
    try:
        font = ImageFont.truetype(font_path, size=font_size)
    except IOError:
        font = ImageFont.load_default()

    # Calculate the bounding box for the header text
    bbox = font.getbbox(header_text)
    title_x = (background_image.width - (bbox[2] - bbox[0])) // 2
    title_y = (header_height - (bbox[3] - bbox[1])) // 2
    draw.text((title_x, title_y), header_text, font=font, fill="white")

    # Calculate the bounding box for the footer text, if provided
    if footer_text:
        bbox_footer = font.getbbox(footer_text)
        footer_x = (background_image.width - (bbox_footer[2] - bbox_footer[0])) // 2
        footer_y = (
            background_image.height
            - footer_height
            + (footer_height - (bbox_footer[3] - bbox_footer[1])) // 2
        )
        draw.text((footer_x, footer_y), footer_text, font=font, fill="black")

    return background_image
