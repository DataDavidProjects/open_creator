import textwrap
from dataclasses import dataclass
from typing import Tuple

from PIL import Image, ImageDraw


@dataclass
class LayoutInfographic:

    """
    Create a generic canvas for an infographic


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
        self, top_left: Tuple[int, int], bottom_right: Tuple[int, int], color: str
    ):
        """
        Crate section given coordinates.

        Args:
            top_left (Tuple(int,int)): start point of bounding box
            bottom_right (Tuple(int,int)): end point of bounding box
            color (str): color of canvas

        Raises:
            ValueError: Canvas is not defined

        Returns:
            self: for chain operation
        """
        if self.canvas is None:
            raise ValueError("Canvas not created.")
        if not color.startswith("#"):
            color = "#" + color

        draw = ImageDraw.Draw(self.canvas)
        draw.rectangle([top_left, bottom_right], fill=color)
        return self

    def add_text(
        self,
        text,
        position,
        loaded_font,
        color,
        max_width,
        alignment="left",
        line_space=5,
        char_space=0,
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


def create_placeholder_image(size, color):
    """Create a simple placeholder image"""
    img = Image.new("RGB", size, color)
    return img


################################################################################

# # Placeholder image creation
# PLACEHOLDER_IMAGE_SIZE = (500, 500)
# PLACEHOLDER_IMAGE_COLOR = "#0000FF"

# # Create placeholder image
# placeholder_image = create_placeholder_image(
#     PLACEHOLDER_IMAGE_SIZE, PLACEHOLDER_IMAGE_COLOR
# )
# # Define Canvas
# CANVAS_WIDTH = 1200
# CANVAS_HEIGHT = 1800

# # Define colors
# BACKGROUND_INFOGRAPHIC = "#FFFFFF"
# TEXT_COLOR = "#000000"
# PRODUCT_BACKGROUND_COLOR = "#EFEFEF"

# # Fonts
# MAIN_FONT = ImageFont.truetype("arial.ttf", 20)
# TITLE_FONT = ImageFont.truetype("arial.ttf", 30)

# # Constants for layout proportions
# HEADER_RATIO = 0.1
# FOOTER_RATIO = 0.1

# # Margins and Padding
# MARGIN_LEFT = 20
# MARGIN_RIGHT = 20
# MARGIN_TOP = int(CANVAS_HEIGHT * HEADER_RATIO)
# MARGIN_BOTTOM = int(CANVAS_HEIGHT * FOOTER_RATIO)
# PADDING = 20  # Padding between header/footer and the product grid
# GRID_PADDING = 10  # Padding between products in the grid

# # Adjusted dimensions for main content with padding
# CONTENT_HEIGHT = int(CANVAS_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - 2 * PADDING)
# CONTENT_WIDTH = CANVAS_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
# CONTENT_START_X = MARGIN_LEFT
# CONTENT_START_Y = MARGIN_TOP + PADDING

# # Header and Footer
# HEADER_SECTION = (0, 0), (CANVAS_WIDTH, MARGIN_TOP)
# HEADER_COLOR = "#4682b4"
# HEADER_TEXT = "Product Catalog"
# HEADER_TEXT_POSITION = (20, 20)

# FOOTER_SECTION = (0, CANVAS_HEIGHT - MARGIN_BOTTOM), (CANVAS_WIDTH, CANVAS_HEIGHT)
# FOOTER_COLOR = "#4682b4"
# FOOTER_TEXT = "© 2023 Company Name"
# FOOTER_TEXT_POSITION = (20, CANVAS_HEIGHT - MARGIN_BOTTOM + 10)

# # Grid layout for products with margins and padding
# NUM_ROWS = 2
# NUM_COLS = 2
# PRODUCT_SECTION_HEIGHT = int(
#     (CONTENT_HEIGHT - (NUM_ROWS - 1) * GRID_PADDING) / NUM_ROWS
# )
# PRODUCT_SECTION_WIDTH = int((CONTENT_WIDTH - (NUM_COLS - 1) * GRID_PADDING) / NUM_COLS)


# # Create canvas
# infographic = (
#     LayoutInfographic()
#     .create_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, BACKGROUND_INFOGRAPHIC)
#     .create_section(*HEADER_SECTION, color=HEADER_COLOR)
#     .create_section(*FOOTER_SECTION, color=FOOTER_COLOR)
#     .add_text(
#         HEADER_TEXT,
#         HEADER_TEXT_POSITION,
#         TITLE_FONT,
#         TEXT_COLOR,
#         CANVAS_WIDTH,
#         alignment="left",
#     )
#     .add_text(
#         FOOTER_TEXT,
#         FOOTER_TEXT_POSITION,
#         MAIN_FONT,
#         TEXT_COLOR,
#         CANVAS_WIDTH,
#         alignment="left",
#     )
# )


# # Add product sections with margins
# for row in range(NUM_ROWS):
#     for col in range(NUM_COLS):
#         top_left = (
#             CONTENT_START_X + col * PRODUCT_SECTION_WIDTH,
#             CONTENT_START_Y + row * PRODUCT_SECTION_HEIGHT,
#         )
#         bottom_right = (
#             top_left[0] + PRODUCT_SECTION_WIDTH,
#             top_left[1] + PRODUCT_SECTION_HEIGHT,
#         )
#         infographic.create_section(top_left, bottom_right, PRODUCT_BACKGROUND_COLOR)

#         # Add placeholder text
#         product_text = f"Product {row * NUM_COLS + col + 1}"
#         product_text_position = (top_left[0] + 10, top_left[1] + 10)
#         infographic.add_text(
#             product_text,
#             product_text_position,
#             MAIN_FONT,
#             TEXT_COLOR,
#             PRODUCT_SECTION_WIDTH,
#             alignment="left",
#         )

#         # Add placeholder image
#         image_position = (top_left[0] + 10, top_left[1] + 50)

#         infographic.add_image(placeholder_image, image_position)

# # Show the canvas
# infographic.canvas.show()


################################################################################


print("Created Canvas")
