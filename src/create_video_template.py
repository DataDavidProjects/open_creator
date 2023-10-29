from creation_caption import create_caption, create_caption_bulk
from creation_infographic import create_captioned_image
from processing.image_processing import get_random_image_path
from processing.video_processing import (
    process_images_and_create_video,
)
import numpy as np
import time
import yaml
from config.config_utils import load_config

start = time.time()


major_config = load_config("src/config/config.yaml")
project = major_config["project"]
minor_config = load_config(f"src/config/{project}/config.yaml")
params = {**major_config, **minor_config}

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
Create a short punchline inspiring quote about {topic} in {language}. 
It should fit the mood of a {social_media} post and contain high traffic keywords for {topic}.
{avoid_prompt}
Try to use terms and keywords that have high SEO on {social_media}.
Create the content only in {language}.
Provide only the content with no additional content.

example:
Art is not a luxury, but a necessity.
YOU ONLY LIVE ONCE.
THIS IS WHY I WORK HARD.
"""


# video
path_to_video = params["path"]["path_to_video"].format(project)
path_to_images = f"src/data/{project}/pins"
video_duration = params["video_processing"]["video_duration"]
frame_rate = params["video_processing"]["frame_rate"]

start = time.time()
# Suggested 1920x1080
n_videos = 2
video_caption = ""  # create_caption(prompt)
for v in range(n_videos):
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
            save_to=f"src/data/{project}/pins/{project}_template_{idx}.png",
            text_color=text_color,
            font_size=font_size,
            wrap_block=wrap_block,
        )

        # Append the captioned image to the img_list
        img_list.append(captioned_image)

    process_images_and_create_video(
        path_to_images,
        f"output_video_{v}.mp4",
        path_to_video,
        video_duration=video_duration,
        resize=True,
        frame_rate=frame_rate,
    )
end = time.time()
print(f"Execution in {end-start} seconds")
