import sys

sys.path.append(".")

import functools
import random

from src.processing.image_processing import *
from src.processing.video_processing import create_video_from_images
from src.utils.authentication import *
from src.utils.file_operations import load_config, read_images

# Config
project_name = PROJECT_NAME
config = load_config(project_name)

root = "src/assets/data/aesthetic_destinations/tiktok/"

# Effects
alpha = config["image_processing"]["alpha_overlay"]
color_overlay = config["image_processing"]["color_overlay"]
color_portrait = config["image_processing"]["color_portrait"]

image_effect_dict = {
    "portrait": functools.partial(apply_portrait, color=color_portrait),
    "overlay": functools.partial(apply_overlay, color=color_overlay, alpha=alpha),
    "blur": functools.partial(apply_blur, None),
    "padding": apply_padding,
}


# read images
images = read_images(path=root + "images")

# padd images
padded_images = [image_effects(i, "padding", image_effect_dict) for i in images]


# create videos
for v in range(3):
    random.shuffle(padded_images)
    create_video_from_images(
        images=padded_images,
        video_name=f"output_video_{v}.mp4",
        output_dir=root + "videos",
        duration=5,
        frame_rate=100,
    )
