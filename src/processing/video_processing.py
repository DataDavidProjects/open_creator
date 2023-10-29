import os

import cv2
import numpy as np


def create_video_from_images(images, video_name, output_dir, duration, frame_rate):
    """
    Creates a video from a list of images with the specified frame rate and duration.

    Parameters:
    - images (list of np.array): A list of images where each image is represented as a numpy array with shape (height, width, channels).
    - video_name (str): The desired name of the output video file including its extension (e.g., "video.mp4").
    - output_dir (str): The directory where the resulting video file will be saved.
    - duration (int or float): The desired duration of the output video in seconds.
    - frame_rate (int): The frame rate of the output video in frames per second (fps).

    The function will determine the number of frames per image based on the desired duration, frame rate, and the number of images.

    If the video writer fails to open, a message will be printed to the console.

    Returns:
    None
    """
    os.makedirs(output_dir, exist_ok=True)
    video_path = os.path.join(output_dir, video_name)

    # Convert the first PIL image to numpy array
    image_array = np.array(images[0])
    height, width, layers = image_array.shape
    frames_per_image = (frame_rate * duration) // len(images)

    video = cv2.VideoWriter(
        video_path, cv2.VideoWriter_fourcc(*"mp4v"), frame_rate, (width, height)
    )
    if not video.isOpened():
        print(f"Failed to open video writer")
        return

    for pil_image in images:
        image_array = np.array(pil_image)  # Convert PIL Image to numpy array
        bgr_image = cv2.cvtColor(
            image_array, cv2.COLOR_RGB2BGR
        )  # Convert RGB to BGR for OpenCV
        for _ in range(frames_per_image):
            video.write(bgr_image)

    video.release()
