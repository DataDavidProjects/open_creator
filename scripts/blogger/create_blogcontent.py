import json
import sys

sys.path.append(".")


import os
import time

from dotenv import load_dotenv

from src.processing.text_processing import Blogger

# time start
start_time = time.time()

# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")

# Initialize the Blogger class with the API key and specify the tone and template path
template_file_path = (
    "./templates/blog_template.html"  # Make sure to use your actual template path
)
output_file_path = (
    "scripts/blogger/blog.html"  # The path where you want to save the rendered HTML
)

blogger = Blogger(api_key, tone="Friendly", template_file_path=template_file_path)
topic = "Dubai"
title = blogger.generate_title(topic)

# Intro
introduction = blogger.generate_introduction(topic)
aspects = [
    (
        """
        Suites in Dubai 
        Luxurious spaces with private balconies overlooking the unrivalled cityscape of Dubai and the iconic Burj Khalifa tower. 
        """,
        "https://www.anantara.com/en/downtown-dubai/rooms/anantara-burj-khalifa-view-suite",
    ),
    (
        "Burj Khalifa",  # Section with a promotion
        "https://www.anantara.com/en/downtown-dubai/rooms/deluxe-burj-khalifa-view-room",
    ),
    # Add more sections as needed
]

# Generate the main content, with promotions turned on
main_content_sections = blogger.generate_main_content(topic, aspects, promo_on=True)


# Save the checkpoint data in a JSON file

checkpoint_filename = "./checkpoint.json"

with open(checkpoint_filename, "w") as f:
    json.dump(main_content_sections, f, indent=4)


print(main_content_sections)
promo_links = [
    section.get("promo", {}).get("link", "")
    for section in main_content_sections
    if section.get("promo")
]

# Make sure each link is structured properly for the template
structured_promo_links = [
    {
        "href": section.get("promo", {}).get("link", ""),
        "text": section.get("promo", {}).get("alt_text", "Click me!"),
    }
    for section in main_content_sections
    if section.get("promo")
]

# Generate the recap and ending, using the main content sections to inform the promo link text generation and the ending content
ending_info = blogger.generate_ending(structured_promo_links, main_content_sections)

# Structure the blog content for rendering
blog_content = {
    "title": title,
    "introduction": introduction,
    "sections": main_content_sections,
    "ending": ending_info,
}
# Render the blog post and write it to an HTML file
blogger.render_blog_post(blog_content, template_file_path, output_file_path)

# time end
end_time = time.time()

# Execution time
print(f"Execution time: {end_time - start_time} seconds")
