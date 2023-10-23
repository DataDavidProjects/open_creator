from creation_caption import create_caption, create_caption_bulk
from creation_infographic import create_captioned_image
from processing.image_processing import get_random_image_path

import numpy as np
import time
import yaml


start = time.time()


# Load parameters from YAML file
with open("config.yaml", "r") as file:
    params = yaml.safe_load(file)

# Assign parameters to variables
project = params["project"]

topic = params["topic"]
language = params["language"]
example = params["example"]
caption_style = params["caption_style"]
social_media = params["social_media"]
sep = params["sep"]

line_text = params["line_text"]
wrap_block = params["font"]["wrap_block"]
path_to_font = params["path"]["path_to_font"]
font = params["font"]["font_type"]
font_path = path_to_font + font

text_color = params["font"]["text_color"]
font_size = params["font"]["font_size"]
background_dir = params["background_dir"].format(project)


avoid_prompt = params["avoid_prompt"]

# Create Quotes Data
n = params["create"]
prompt = f"""
Provide me a list of {n}  {line_text}  {caption_style} about {topic} in {language}. 
They should fit the mood of a {social_media} post and contain high traffic keywords for {topic}.
Separate each quote using a {sep} .
{avoid_prompt}
Try to use terms and keywords that have high SEO on {social_media}.
Create the content only in {language}.
Provide only the list with no additional content.

Example output:
{example}
"""


data = create_caption_bulk(prompt=prompt).replace("", np.nan).dropna()

# Modify string
data["caption"] = data["caption"].str.strip()  # .str.upper()

# Create an empty list to store the images
img_list = []

# Iterate over the captions using a normal for loop
for idx, caption in enumerate(data["caption"]):
    # Get a random image path
    img_path = get_random_image_path(background_dir)

    # Create the captioned image
    captioned_image = create_captioned_image(
        caption=caption,
        font_path=font_path,
        img_path=img_path,
        save_to=f"./data/{project}/pins/{project}_template_{idx}.png",
        text_color=text_color,
        font_size=font_size,
        wrap_block=wrap_block,
    )

    # Append the captioned image to the img_list
    img_list.append(captioned_image)

data["images"] = img_list

end = time.time()
print(f"Execution in {end-start} seconds")
# Save data
data.to_csv(f"./data/{project}/tables/quotes.csv", sep=",", index=False)
