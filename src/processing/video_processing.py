from PIL import Image
import cv2
import os
import numpy as np
import yaml
from processing.image_processing import resize_image, read_image
from typing import Optional, Tuple, Union

# Load parameters from YAML file
with open("config.yaml", "r") as file:
    params = yaml.safe_load(file)


def check_image_sizes(image_paths):
    sizes = {Image.open(img_path).size for img_path in image_paths}
    return len(sizes) == 1, sizes.pop() if len(sizes) == 1 else None


def load_and_resize_images(image_folder, width=None):
    images = []
    for img_name in os.listdir(image_folder):
        if img_name.endswith(".png"):
            with Image.open(os.path.join(image_folder, img_name)) as img:
                if width is not None:
                    img = resize_image(img, width=width)
                images.append(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
    return images


frame_rate = params["video_processing"]["frame_rate"]


def create_video_from_images(
    images, video_name, output_dir, duration, frame_rate=frame_rate
):
    os.makedirs(output_dir, exist_ok=True)
    video_path = os.path.join(output_dir, video_name)

    height, width, layers = images[0].shape
    frames_per_image = (frame_rate * duration) // len(images)

    video = cv2.VideoWriter(
        video_path, cv2.VideoWriter_fourcc(*"mp4v"), frame_rate, (width, height)
    )
    if not video.isOpened():
        print(f"Failed to open video writer")
        return

    for image in images:
        for _ in range(frames_per_image):
            video.write(image)

    video.release()


width_resize = params["video_processing"]["width_resize"]


def process_images_and_create_video(
    image_folder: str,
    video_name: str,
    output_dir: str,
    duration: int = 5,
    resize: bool = False,
    frame_rate: int = 30,
    max_size: Optional[Tuple[int, int]] = None,
) -> None:
    images = []
    for img_name in os.listdir(image_folder):
        if img_name.endswith(".png"):
            image_path = os.path.join(image_folder, img_name)
            img = read_image(image_path)
            if resize and max_size is not None:
                img = resize_image(img, max_size=max_size)
            images.append(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

    same_size, img_size = check_image_sizes(
        [
            os.path.join(image_folder, img)
            for img in os.listdir(image_folder)
            if img.endswith(".png")
        ]
    )

    if not same_size and not resize:
        raise ValueError(
            "Images are not the same size and resize option is set to False."
        )

    else:
        images = load_and_resize_images(image_folder)  # No resizing needed

    create_video_from_images(images, video_name, output_dir, duration, frame_rate)
