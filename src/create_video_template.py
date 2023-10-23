from creation_caption import create_caption, create_caption_bulk
from creation_infographic import create_captioned_image
from processing.image_processing import get_random_image_path
from processing.video_processing import process_images_and_create_video
import numpy as np
import time
import yaml


start = time.time()


# Load parameters from YAML file
with open("config.yaml", "r") as file:
    params = yaml.safe_load(file)

# Assign parameters to variables
project = params["project"]
background_dir = params["background_dir"].format(project)

# caption
text_color = params["font"]["text_color"]
font_size = params["font"]["font_size"]
wrap_block = params["font"]["wrap_block"]
path_to_font = params["path"]["path_to_font"]
font = params["font"]["font_type"]
font_path = path_to_font + font


# Create an empty list to store the images
img_list = []

video_caption = "PIXEL POSE MONEY"
n = params["create"]
# Iterate over the captions using a normal for loop
for idx in range(n):
    # Get a random image path
    img_path = get_random_image_path(background_dir)

    # Create the captioned image
    captioned_image = create_captioned_image(
        caption=video_caption,
        font_path=font_path,
        img_path=img_path,
        save_to=f"./data/{project}/pins/{project}_template_{idx}.png",
        text_color=text_color,
        font_size=font_size,
        wrap_block=wrap_block,
    )

    # Append the captioned image to the img_list
    img_list.append(captioned_image)


# video
path_to_video = params["path"]["path_to_video"].format(project)
path_to_images = f"data/{project}/pins"
video_name = "output_video.mp4"
video_duration = params["video_processing"]["video_duration"]

# Suggested 1920x1080
process_images_and_create_video(
    path_to_images, video_name, path_to_video, duration=video_duration, resize=True
)
