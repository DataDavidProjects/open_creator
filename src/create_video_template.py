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


# style prompt
caption_style = params["caption_style"]
social_media = params["social_media"]
sep = params["sep"]
topic = params["topic"]
language = params["language"]
avoid_prompt = params["avoid_prompt"]

# caption
text_color = params["font"]["text_color"]
font_size = params["font"]["font_size"]
wrap_block = params["font"]["wrap_block"]
path_to_font = params["path"]["path_to_font"]
font = params["font"]["font_type"]
font_path = path_to_font + font
line_text = params["line_text"]


# Create Quotes Data
example = params["example"]
prompt = f"""
Create one  {line_text}  {caption_style} about {topic} in {language}. 
It should fit the mood of a {social_media} post and contain high traffic keywords for {topic}.
{avoid_prompt}
Try to use terms and keywords that have high SEO on {social_media}.
Create the content only in {language}.
Provide only the content with no additional content.

Example of possible outputs:
{example}
"""

video_caption = create_caption(prompt)


# Create an empty list to store the images
img_list = []

images_in_video = params["video_processing"]["images_in_video"]
# Iterate over the captions using a normal for loop
for idx in range(images_in_video):
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
frame_rate = params["video_processing"]["frame_rate"]
# Suggested 1920x1080
process_images_and_create_video(
    path_to_images,
    video_name,
    path_to_video,
    duration=video_duration,
    resize=True,
    frame_rate=frame_rate,
)
