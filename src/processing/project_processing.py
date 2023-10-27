import argparse
import os
import yaml


def load_params(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


def create_directories(project: str):
    os.makedirs(f"./data/{project}", exist_ok=True)
    os.makedirs(f"./config/{project}", exist_ok=True)
    os.makedirs(f"./data/{project}/videos", exist_ok=True)
    os.makedirs(f"./data/{project}/videos/images", exist_ok=True)
    os.makedirs(f"./data/{project}/background", exist_ok=True)
    os.makedirs(f"./data/{project}/pins", exist_ok=True)

    # Specify the content for config.yaml
    config_content = """
avoid_prompt: >
  Do not write false informations
  Do not use emojis or hastags!.
  Do not leave empty spaces between each line
  Do not exceed the request number

example: >
  "....... \\n"

line_text: "oneline"
sep: "\\n"

font:
  font_type: "HATTEN.TTF"
  text_color: "#FFFF"
  font_size: 90
  wrap_block: 50
  text_coords:
    auto: True
    width: 180 #if auto is False
    height: 500 #if auto is False
    align: "left"

path:
  path_to_image: "src/data/{}/background/{}_template_{}.png"
  path_to_font: "src/fonts/"
  path_to_video: "src/data/{}/videos"

image_processing:
  alpha_overlay: 0.1
  color_overlay: "#0000"
  color_portrait: "#FFFFFF"

video_processing:
  frame_rate: 15
  video_duration: 10
  images_in_video: 10
  width_resize: 800
    """.format(
        project, project, project, project
    )  # Replace placeholders with project name

    # Create and write to config.yaml
    with open(f"./config/{project}/config.yaml", "w") as config_file:
        config_file.write(config_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a project.")
    parser.add_argument("project", type=str, help="The name of the project")
    args = parser.parse_args()
    create_directories(args.project)
