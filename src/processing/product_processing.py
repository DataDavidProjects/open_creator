import os
import random
import shutil
import sys
import textwrap
from dataclasses import dataclass
from typing import List, Tuple, Union

from PIL import Image, ImageDraw, ImageFont

from src.processing.image_processing import (
    create_grid_infographic,
    fill_transparency,
    pad_image_to_size,
    reduce_size,
)
from src.processing.text_processing import draw_multiline_text, draw_text_with_spacing
from src.utils.file_operations import read_images

sys.path.append(".")


def image_grid_processing(path: str):
    original_products = read_images(path=path)
    products = [
        pad_image_to_size(
            reduce_size(fill_transparency(img=i), size=(400, 400)), (410, 410)
        )
        for i in original_products
    ]
    return products


def create_product_grid(background_image_path: str, product_path: str, title: str):
    products = image_grid_processing(path=product_path)

    # Sample 9 images without replacement
    n = 9
    if len(products) >= n:
        image_list = random.sample(products, n)
    else:
        raise ValueError(
            f"Not enough images to sample: {len(products)} available, {n} required."
        )

    # Create the infographic
    infographic = create_grid_infographic(
        background_path=background_image_path,
        images=image_list,
        header_text=title,
        header_height=200,
        font_size=50,
        font_path="src/assets/fonts/Montserrat_700.ttf",
    )

    return infographic


def create_mix(
    categories: List[str], output_base: str, n: int = 9, destination_folder="products"
) -> None:
    """
    Creates a directory and populates it with a specified number of items randomly picked from given categories.

    Parameters:
    categories (List[str]): A list of category names to pick products from.
    output_base (str): The base directory where the content directory and product categories are located.
    n (int): The number of items to pick and copy into the mix directory.

    Returns:
    None
    """

    # Creating a new mix directory with a name based on the provided categories
    mix_dir_name = "Mix_" + "_".join(categories)
    mix_directory = os.path.join(output_base, destination_folder, mix_dir_name)
    os.makedirs(mix_directory, exist_ok=True)

    # Initialize a list to hold all product file paths
    all_products = []

    # Iterate over each category to collect file paths of products
    for cat in categories:
        cat_dir = os.path.join(output_base, destination_folder, cat)
        for prod in os.listdir(cat_dir):
            # Check if the path is a file, not a subdirectory
            if os.path.isfile(os.path.join(cat_dir, prod)):
                all_products.append((cat, prod))

    # Randomly sample products to be copied to the mix directory
    selected_products = random.sample(all_products, n)

    # Copy each selected product to the newly created mix directory
    for cat, product in selected_products:
        product_path = os.path.join(output_base, destination_folder, cat, product)
        shutil.copy(product_path, os.path.join(mix_directory, product))

    return selected_products


def image_collect(
    root: str,
    n: int,
    subdir: List[str],
    suffixes: List[str] = [".png", ".jpg", ".jpeg", ".bmp", ".gif"],
) -> List[Tuple[Image.Image, str]]:
    image_list = []
    # Dictionary to keep track of images in each subdirectory
    images_in_subdir = {s: [] for s in subdir}

    # Pre-populate the dictionary with available images in each subdir
    for sub in subdir:
        full_path = os.path.join(root, sub)
        if os.path.isdir(full_path):
            # List all files and filter by suffixes
            images_in_subdir[sub] = [
                f for f in os.listdir(full_path) if f.lower().endswith(tuple(suffixes))
            ]

    # Randomly select images from the pre-populated list
    while len(image_list) < n:
        # print("Searching...")
        for sub in subdir:
            if images_in_subdir[sub]:  # If there are images left in this subdir
                chosen_file = random.choice(images_in_subdir[sub])
                images_in_subdir[sub].remove(
                    chosen_file
                )  # Remove the chosen file to prevent re-selection
                file_path = os.path.join(root, sub, chosen_file).replace("\\", "/")
                try:
                    with Image.open(file_path) as img:
                        image_list.append(
                            (
                                pad_image_to_size(
                                    reduce_size(
                                        fill_transparency(img=img),
                                        size=(220, 235),
                                    ),
                                    (230, 245),
                                ),
                                file_path,
                            )
                        )
                        if len(image_list) == n:
                            return image_list
                except Exception as e:
                    print(f"Failed to open file {file_path}: {e}")

    return image_list


@dataclass
class ProductsInfographic:
    canvas: Image = None

    def create_canvas(self, w: int, h: int, color: str, image_path: str = None):
        # Create canvas with the specified color
        if not color.startswith("#"):
            color = "#" + color
        self.canvas = Image.new("RGB", (w, h), color)

        # If an image path is provided, open and paste the image
        if image_path is not None:
            with Image.open(image_path) as img:
                # Optionally resize or process the image
                img = img.resize((w, h))

                # Paste the image onto the canvas
                self.canvas.paste(img, (0, 0))

        return self

    def create_section(
        self, top_left: Tuple[int, int], bottom_right: Tuple[int, int], color: str
    ):
        if self.canvas is None:
            raise ValueError("Canvas not created.")
        if not color.startswith("#"):
            color = "#" + color

        draw = ImageDraw.Draw(self.canvas)
        draw.rectangle([top_left, bottom_right], fill=color)
        return self

    def add_header(
        self,
        height,
        color="#6f42c1",
        text="",
        title_font_path="arial.ttf",
        title_font_size=24,
        text_color="black",
    ):
        # Create the header section
        self.create_section((0, 0), (self.canvas.width, height), color)

        if text:  # Check if any text is provided
            draw = ImageDraw.Draw(self.canvas)
            font = ImageFont.truetype(title_font_path, title_font_size)

            # Calculate maximum text width
            max_text_width = (
                self.canvas.width + 100
            )  # Assuming a padding of 10 on each side

            # Calculate the position to start the text
            text_position = (50, 80)  # Starting 10 pixels in from the top-left corner

            # Draw the multiline text
            draw_multiline_text(
                draw,
                text_position,
                text,
                font,
                text_color,
                max_text_width,
                alignment="left",
            )

            font = ImageFont.truetype("arial.ttf", title_font_size / (1.68 * 1.8))
            # Draw the multiline text
            letter_spacing = 20
            draw_text_with_spacing(
                draw, (400, 180), "GIFT GUIDES", font, "black", letter_spacing
            )

    def add_footer(
        self,
        height,
        color="#6f42c1",
        text="",
        title_font_path="arial.ttf",
        title_font_size=24,
        text_color="black",
    ):
        self.create_section(
            (0, self.canvas.height - height),
            (self.canvas.width, self.canvas.height),
            color,
        )
        if text:  # Check if any text is provided
            draw = ImageDraw.Draw(self.canvas)
            font = ImageFont.truetype(title_font_path, title_font_size)

            # Calculate maximum text width
            max_text_width = (
                self.canvas.width - 5
            )  # Assuming a padding of 10 on each side

            # Calculate the position to start the text
            text_position = (
                150,
                1700,
            )  # Starting 10 pixels in from the top-left corner

            # Draw the multiline text
            # draw_multiline_text(
            #     draw,
            #     text_position,
            #     text,
            #     font,
            #     text_color,
            #     max_text_width,
            #     alignment="center",
            # )
            letter_spacing = 10
            draw_text_with_spacing(
                draw, text_position, text, font, "black", letter_spacing
            )

            text_width, text_height = font.getbbox(text)[2], font.getbbox(text)[3]

            # Calculate the bounding box of the text
            text_bbox = font.getbbox(text)
            text_width = text_bbox[2]
            text_height = text_bbox[3]

            # Calculate the position to start the text
            text_x = (self.canvas.width - text_width) // 2
            text_y = self.canvas.height - height + (height - text_height) // 2

            # Positions for the top and bottom lines relative to the text
            line_top_y = text_y - (
                title_font_size // 4
            )  # Adjust the division factor as needed for desired spacing
            line_bottom_y = (
                text_y + text_height + (title_font_size // 4)
            )  # Adjust accordingly

            # Adjust the line start and end positions if needed
            line_start_x = text_x - (title_font_size // 4)
            line_end_x = text_x + text_width + (title_font_size // 4)

            # Draw the top line
            draw.line(
                [(line_start_x - 250, line_top_y), (line_end_x + 250, line_top_y)],
                fill="black",
                width=1,
            )

            # Draw the bottom line
            draw.line(
                [
                    (line_start_x - 250, line_bottom_y),
                    (line_end_x + 250, line_bottom_y),
                ],
                fill="black",
                width=1,
            )

    def add_text(self, text, position, font, color, max_width, alignment="left"):
        if self.canvas is None:
            raise ValueError("Canvas not created.")
        draw = ImageDraw.Draw(self.canvas)
        text = textwrap.fill(text, width=max_width)
        draw.text(position, text, font=font, fill=color)
        return self

    def add_product_card(
        self,
        section_top_left: Tuple[int, int],
        section_bottom_right: Tuple[int, int],
        title: str,
        product_image: Image,
        description: str,
        title_font_path: str,
        desc_font_path: str,
        title_font_size: int,
        desc_font_size: int,
    ):
        if self.canvas is None:
            raise ValueError("Canvas not created.")

        section_width = section_bottom_right[0] - section_top_left[0]
        padding = 5  # Padding from the edge of the section

        title_font = ImageFont.truetype(title_font_path, title_font_size)
        desc_font = ImageFont.truetype(desc_font_path, desc_font_size)

        title_pos = (section_top_left[0] + padding, section_top_left[1] + padding)
        image_pos = (
            section_top_left[0] + padding,
            title_pos[1] + title_font.getbbox(title)[3] + padding,
        )

        max_text_width = section_width - (2 * padding)

        draw = ImageDraw.Draw(self.canvas)

        # Draw title
        draw_multiline_text(
            draw,
            title_pos,
            title,
            title_font,
            "black",
            max_text_width,
            alignment="center",
        )

        # Resize and paste the image
        image_area_height = int(
            (section_bottom_right[1] - section_top_left[1]) * 0.70
        )  # 70% of the card height

        self.canvas.paste(product_image, (image_pos[0] - 0, image_pos[1]))

        # Draw description
        desc_pos = (
            section_top_left[0] + padding,
            image_pos[1] + image_area_height + padding,
        )
        draw_multiline_text(
            draw,
            desc_pos,
            description,
            desc_font,
            "black",
            max_text_width,
            alignment="center",
        )

        # Calculate the bounding box of the description text
        text_bbox = desc_font.getbbox(description, anchor="lt")
        line_y_position = (
            desc_pos[1] + text_bbox[3] + padding // 2
        )  # Adjust the position of the line to be under the text

        # Draw design line under the description
        # draw.line(
        #     [
        #         (section_top_left[0] + 80, line_y_position + 50),
        #         (section_bottom_right[0] - 80, line_y_position + 50),
        #     ],
        #     fill="black",
        #     width=1,
        # )

        return self


def create_grid_positions(
    canvas_width,
    canvas_height,
    num_columns,
    num_rows,
    header_height,
    footer_height,
    margin,
    vertical_margin,
):
    card_width = (canvas_width - (num_columns + 1) * margin) // num_columns
    card_height = (
        canvas_height - header_height - footer_height - (num_rows - 1) * vertical_margin
    ) // num_rows
    positions = []
    for row in range(num_rows):
        for col in range(num_columns):
            top_left_x = col * (card_width + margin) + margin
            top_left_y = row * (card_height + vertical_margin) + header_height + margin
            bottom_right_x = top_left_x + card_width
            bottom_right_y = top_left_y + card_height
            positions.append(
                ((top_left_x, top_left_y), (bottom_right_x, bottom_right_y))
            )
    return positions


@dataclass
class Infographic:

    """
    Create a generic canvas for infographic.


    Returns:
        Image: canvas after operations
    """

    canvas: Image = None

    def create_canvas(self, w: int, h: int, color: str):
        """
        Create a canvas given args.

        Args:
            w (int): width of canvas
            h (int): height of canvas
            color (str): color of canvas

        Returns:
            self: for chain operation
        """
        if not color.startswith("#"):
            color = "#" + color
        self.canvas = Image.new("RGB", (w, h), color)
        return self

    def create_section(
        self,
        coordinates: List[Tuple[int, int]],
        color: str,
        corners: Union[int, str, None] = None,
        line_color: str = None,
        line_width: int = 0,
    ):
        """
        Create a section given coordinates with optional rounded corners or a circle.

        Args:
            coordinates (List[Tuple[int, int]]): List of two tuples defining the top-left and bottom-right points.
            color (str): Fill color of the section.
            corners (Union[int, str, None]): Radius of the rounded corners, or 'circle' for a full circle.
            line_color (str, optional): Color of the line if corners are rounded or circle is drawn.
            line_width (int, optional): Thickness of the line if corners are rounded or circle is drawn.
        """
        if self.canvas is None:
            raise ValueError("Canvas not created.")

        draw = ImageDraw.Draw(self.canvas)
        top_left, bottom_right = coordinates
        left, top = top_left
        right, bottom = bottom_right

        if corners == "circle":
            # Calculate radius for a circle
            width = right - left
            height = bottom - top
            radius = min(width, height) // 2
            center = (left + radius, top + radius)
            draw.ellipse(
                [
                    center[0] - radius,
                    center[1] - radius,
                    center[0] + radius,
                    center[1] + radius,
                ],
                fill=color,
                outline=line_color,
                width=line_width,
            )
        elif corners is not None:
            # Draw a rounded rectangle
            draw.rounded_rectangle(
                [top_left, bottom_right],
                fill=color,
                radius=corners,
                outline=line_color,
                width=line_width,
            )
        else:
            # Draw a regular rectangle if no corners are specified
            draw.rectangle([top_left, bottom_right], fill=color)

        return self

    def add_text(
        self,
        text: str,
        position: List[Tuple[int, int]],
        loaded_font,
        color: str,
        max_width: int = 100,
        alignment="left",
        line_space: int = 5,
        char_space: int = 0,
    ):
        """
        Add text to the infographic with specified formatting.

        Args:
            text (str): Text to be added.
            position (Tuple[int, int]): Starting coordinates for the text.
            loaded_font (ImageFont): Font to be used for the text.
            color (str): Color of the text.
            max_width (int): Maximum width for text wrapping.
            alignment (str): Alignment of the text ('left', 'center', 'right').
            line_space (int): Space between lines.
            char_space (int): Space between characters.
        """
        draw = ImageDraw.Draw(self.canvas)

        # Wrap text to fit within the specified width.
        single_char_bbox = loaded_font.getbbox("A")
        single_char_width = single_char_bbox[2] - single_char_bbox[0]
        max_chars_per_line = int(max_width // (single_char_width + char_space))
        wrapped_text = textwrap.wrap(text, width=max_chars_per_line)

        x, y = position
        for line in wrapped_text:
            if char_space != 0:
                # Draw text with character spacing
                for char in line:
                    draw.text((x, y), char, font=loaded_font, fill=color)
                    char_width = loaded_font.getbbox(char)[2]
                    x += char_width + char_space
            else:
                # Calculate x position based on alignment using font.getbbox
                line_bbox = loaded_font.getbbox(line)
                line_width = line_bbox[2] - line_bbox[0]
                line_height = line_bbox[3] - line_bbox[1]

                if alignment == "center":
                    x = position[0] + (max_width - line_width) // 2
                elif alignment == "right":
                    x = position[0] + max_width - line_width
                else:
                    x = position[0]

                draw.text((x, y), line, font=loaded_font, fill=color)

            # Move to the next line
            y += line_height + line_space

        return self

    def add_image(self, image, position):
        """
        Add an image to the infographic at the specified position.

        Args:
            image (PIL.Image): Image to be added.
            position (tuple): Top-left position where the image will be placed.
        """
        if self.canvas is None:
            raise ValueError("Canvas not created.")

        # Paste the image onto the canvas at the given position
        self.canvas.paste(image, position, mask=image if image.mode == "RGBA" else None)

        return self
