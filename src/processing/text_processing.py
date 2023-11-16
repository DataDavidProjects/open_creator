import sys

sys.path.append(".")

from typing import Any, Dict, List

from openai import OpenAI

from src.utils.authentication import OPENAI_API_KEY, PROJECT_NAME, load_config

config = load_config(project_name=PROJECT_NAME)
api_key = OPENAI_API_KEY


class Blogger:
    def __init__(
        self,
        api_key: str,
    ) -> None:
        self.api_key = api_key

    def completion(
        self,
        prompt: str,
        model="gpt-3.5-turbo-instruct",
        frequency_penalty=0.8,
        temperature=0.5,
    ) -> str:
        """Openai API

        Args:
            prompt (str): direct instructions
            system (str): context for conditioning responses
            stop (str, optional): criteria to avoid in responses. Defaults to None.

        Returns:
            str: response using openai chat completion
        """
        openai_client = OpenAI(api_key=api_key)

        payload = {
            "model": model,
            "temperature": temperature,
            "frequency_penalty": frequency_penalty,
            "prompt": prompt,
            "max_tokens": 800,
            "stop": "Welcome",
        }

        response = openai_client.completions.create(**payload)
        content = response.choices[0].text.strip().replace('"', "")

        return content

    def generate_title(self, topic: str, seo: bool = False) -> str:
        """
        Generates a title for a given topic.

        :param topic: The topic for which to generate a title.
        :param seo: Whether to optimize the title for SEO.
        :return: Generated title.
        """

        instructions = config["blogger"]["blog"]["prompts"]["generate_title"][
            "instructions"
        ]

        prompt = config["blogger"]["blog"]["prompts"]["generate_title"][
            "prompt"
        ].format(topic=topic, instructions=instructions)

        title = self.completion(prompt)
        if seo:
            keywords = self.generate_keywords(topic, n=1)
            title = self.incorporate_keywords(title, keywords)

        return title

    def generate_subtitle(self, topic: str, seo: bool = False) -> str:
        """
        Generates a subtitle for a given topic.

        :param topic: The topic for which to generate a subtitle.
        :param seo: Whether to optimize the subtitle for SEO.
        :return: Generated subtitle.
        """
        instructions = config["blogger"]["blog"]["prompts"]["generate_title"][
            "instructions"
        ]

        prompt = config["blogger"]["blog"]["prompts"]["generate_title"][
            "prompt"
        ].format(topic=topic, instructions=instructions)

        subtitle = self.completion(prompt)
        if seo:
            # Assuming that SEO optimization for a subtitle might involve keyword inclusion or adjustments
            keywords = self.generate_keywords(
                topic, n=3
            )  # Generating a few keywords for the subtitle
            subtitle = self.incorporate_keywords(subtitle, keywords)

        return subtitle

    def generate_introduction(self, topic: str, seo: bool = False) -> str:
        """
        Generates an introduction for a given topic and aspect.

        :param topic: The main topic of the blog post.
        :param aspect: A specific aspect of the topic to focus on in the introduction.
        :param seo: Whether to optimize the introduction for SEO.
        :return: Generated introduction paragraph.
        """
        instructions = config["blogger"]["blog"]["prompts"]["generate_introduction"][
            "instructions"
        ]

        prompt = config["blogger"]["blog"]["prompts"]["generate_introduction"][
            "prompt"
        ].format(topic=topic, instructions=instructions)

        introduction = self.completion(prompt)
        if seo:
            # Optionally, you can optimize the introduction for SEO
            keywords = self.generate_keywords(
                topic, n=3
            )  # Adjust the number of keywords as needed
            introduction = self.incorporate_keywords(introduction, keywords)

        return introduction

    def generate_promo(
        self, content: str, promo_link: str, method: str, seo: bool = False
    ) -> str:
        """
        Generates a promotional paragraph for the given content.

        :param content: The original content.
        :param promo_link: The promotional link to include.
        :param method: The method to incorporate the promo ('append' or 'blend').
        :param seo: Whether to optimize the content for SEO.
        :return: Content with promotional paragraph.
        """
        instructions = config["blogger"]["blog"]["prompts"]["generate_promo"][
            "instructions"
        ]
        prompt = config["blogger"]["blog"]["prompts"]["generate_promo"][
            "prompt"
        ].format(
            content=content,
            promo_link=promo_link,
            method=method,
            instructions=instructions,
        )

        paragraph_promo = self.completion(prompt)
        if seo:
            paragraph_promo = self.optimized_seo(paragraph_promo)

        return paragraph_promo

    def generate_button_link(self, promo_link: str, topic: str) -> str:
        """
        Generates a call-to-action button link text for a given promotional link.

        :param promo_link: The promotional link for which to generate the CTA button text.
        :param topic: The topic related to the promotional link.
        :return: Generated button link text.
        """
        instructions = config["blogger"]["blog"]["prompts"]["generate_button_link"][
            "instructions"
        ]
        prompt = config["blogger"]["blog"]["prompts"]["generate_button_link"][
            "prompt"
        ].format(
            topic=topic,
            promo_link=promo_link,
            instructions=instructions,
        )

        button_link_text = self.completion(prompt)

        return button_link_text

    def generate_paragraph(
        self, topic: str, promo_link: str, subtitle: str = None, seo: bool = False
    ) -> str:
        """
        Generates a paragraph about a given topic.

        :param topic: The topic of the paragraph.
        :param promo_link: Promotional link to include.
        :param subtitle: Optional subtitle for the paragraph.
        :param seo: Whether to optimize the paragraph for SEO.
        :return: Generated paragraph.
        """
        instructions = config["blogger"]["blog"]["prompts"]["generate_promo"][
            "instructions"
        ]
        prompt = config["blogger"]["blog"]["prompts"]["generate_introduction"][
            "prompt"
        ].format(
            topic=topic,
            subtitle=subtitle,
            instructions=instructions,
        )

        paragraph = self.completion(prompt)
        if promo_link:
            paragraph = self.generate_promo(paragraph, promo_link, "off", seo)

        return paragraph

    def generate_recap(self, main_content: List[dict]) -> str:
        """
        Generates a recap or conclusion for the blog post.

        :param main_content: The main content of the blog post.
        :return: Recap or concluding paragraph.
        """

        # Concatenating paragraphs for summary
        content_to_summarize = " ".join(
            [section["paragraph"] for section in main_content]
        )
        instructions = config["blogger"]["blog"]["prompts"]["generate_recap"][
            "instructions"
        ]
        prompt = config["blogger"]["blog"]["prompts"]["generate_recap"][
            "prompt"
        ].format(
            content_to_summarize=content_to_summarize,
            instructions=instructions,
        )

        recap = self.completion(prompt)
        return recap

    def optimized_seo(
        self, content: str, keywords: List[str] = None, topic: str = "", n: int = 5
    ) -> str:
        """
        Optimizes the given content for SEO by incorporating keywords.

        :param content: The original content.
        :param keywords: A list of keywords to incorporate. If None, keywords will be generated.
        :param topic: The topic for keyword generation (used if keywords are None).
        :param n: The number of keywords to generate (used if keywords are None).
        :return: SEO optimized content.
        """
        if keywords is None:
            if not topic:
                raise ValueError("Topic must be provided if keywords are not given.")
            keywords = self.generate_keywords(topic, n)

        return self.incorporate_keywords(content, keywords)

    def generate_section(self, topic: str, promo_link: str, seo: bool = False) -> dict:
        """
        Generates a section of the blog post.

        :param topic: The topic of the section.
        :param promo_link: Promotional link to include.
        :param seo: Whether to optimize the section for SEO.
        :return: A dictionary representing the section.
        """
        subtitle = self.generate_subtitle(topic)
        paragraph = self.generate_paragraph(topic, promo_link, subtitle, seo)

        section = {
            "subtitle": subtitle,
            "paragraph": paragraph,
            "promo_link": promo_link,
        }

        return section

    def generate_main_content(
        self, aspects: List[Dict[str, Any]], seo: bool = False
    ) -> List[dict]:
        """
        Generates the main content of the blog post.

        :param aspects: A list of aspects or topics to cover in the blog.
        :param seo: Whether to optimize the content for SEO.
        :return: A list of sections representing the main content.
        """
        main_content = []
        for aspect in aspects:
            # Generate content
            section = self.generate_section(
                aspect["topic"], aspect.get("promo_link", ""), seo
            )
            # Generate link text for promotions
            if aspect["promo_link"] is not None:
                section["link_text"] = self.generate_button_link(
                    topic=aspect["topic"], promo_link=aspect["promo_link"]
                )

            main_content.append(section)

        return main_content

    def generate_keywords(self, topic: str, n: int) -> List[str]:
        """
        Generates up to n SEO-friendly keywords for a given topic.

        :param topic: The topic for which to generate keywords.
        :param n: The number of keywords to generate.
        :return: A list of generated keywords.
        """

        instructions = config["blogger"]["blog"]["prompts"]["generate_keywords"][
            "instructions"
        ]
        prompt = config["blogger"]["blog"]["prompts"]["generate_keywords"][
            "prompt"
        ].format(
            topic=topic,
            n=n,
            instructions=instructions,
        )

        keywords_str = self.completion(prompt=prompt)
        keywords = keywords_str.split(", ")[:n]
        return keywords

    def incorporate_keywords(self, content: str, keywords: List[str]) -> str:
        """
        Incorporates given keywords into the content in a natural way.

        :param content: The original content.
        :param keywords: A list of keywords to incorporate.
        :return: Content with keywords incorporated.
        """
        instructions = config["blogger"]["blog"]["prompts"]["incorporate_keywords"][
            "instructions"
        ]
        prompt = config["blogger"]["blog"]["prompts"]["incorporate_keywords"][
            "prompt"
        ].format(
            content=content,
            keywords=keywords,
            instructions=instructions,
        )

        optimized_content = self.completion(prompt=prompt)

        return optimized_content


import os

import requests


def download_font(api_key: str, save_to: str, family: str, style: str = "regular"):
    """
    Downloads a specific font style from the Google Fonts API and saves it to a given path.

    Parameters:
    api_key (str): The API key for authenticating with the Google Fonts API.
    save_to (str): The file path where the font should be saved.
    family (str): The font family to download.
    style (str): The style of the font to download (e.g., 'regular', 'italic', '700', etc.).

    Returns:
    None
    """
    # Endpoint for the Google Fonts API
    endpoint = "https://www.googleapis.com/webfonts/v1/webfonts"

    # Parameters to be sent with the API request
    params = {"key": api_key}

    # Perform the GET request to the Google Fonts API
    response = requests.get(endpoint, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        fonts_list = response.json().get("items", [])

        # Find the requested font family
        font_info = next(
            (font for font in fonts_list if font["family"].lower() == family.lower()),
            None,
        )

        if font_info:
            # Check if the requested style is available for the font
            if style.lower() in font_info["variants"]:
                # Construct the URL to download the font
                font_url = font_info["files"][style.lower()]
                # Download the font file
                font_response = requests.get(font_url)
                if font_response.status_code == 200:
                    # Ensure the save_to directory exists
                    os.makedirs(os.path.dirname(save_to), exist_ok=True)

                    file_path = os.path.join(
                        save_to, f"{family.replace(' ', '_')}_{style}.ttf"
                    )

                    # Save the font file
                    with open(file_path, "wb") as font_file:
                        font_file.write(font_response.content)
                    print(
                        f"Font '{family}' with style '{style}' has been downloaded to '{save_to}'."
                    )
                else:
                    raise Exception(
                        f"Failed to download the font, status code: {font_response.status_code}"
                    )
            else:
                raise ValueError(f"Style '{style}' not found for family '{family}'.")
        else:
            raise ValueError(f"Font family '{family}' not found.")
    else:
        raise Exception(f"Failed to fetch fonts, status code: {response.status_code}")


# download_font(
#     "*****",
#     "src/assets/fonts/",
#     "Montserrat",
#     "700",
# )
