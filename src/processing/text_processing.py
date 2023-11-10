import os
import random
from typing import Any, Dict, List, Tuple, Union

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from openai import OpenAI

from src.utils.file_operations import load_config

# Config Project files
project_name = "aesthetic_destinations"
config = load_config(project_name)


# Load environment variables
load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=api_key)  # Load environment variables


class Blogger:
    def __init__(
        self,
        api_key: str,
        system: str = """
        You are an AI experienced in generating creative content for blogs.
        Do not introduce yourself and get to the point.""",
        tone: str = "",
        template_file_path: str = "./blog_template.html",
    ) -> None:
        """
        Initializes the Blogger with an API key and an optional system prompt.

        :param api_key: The API key for OpenAI's API.
        :param system: A predefined system prompt for the AI model.
        """
        self.api_key: str = api_key
        self.system: str = system
        self.tone: str = tone
        self.keywords: List[str] = []
        self.main_content_sections: List[str] = []
        self.template_file_path = template_file_path
        self.context = []

    def make_template(self, template_file_path: str):
        """
        Creates an HTML template skeleton for a blog post and saves it as {file_name}.html.

        :param file_name: The base name of the HTML file to create (without the extension).
        """
        html_template = config["blogger"]["blog"]["hmtl_template"]
        # Write the HTML template to the specified file
        with open(f"{template_file_path}", "w") as file:
            file.write(html_template)

    def render_blog_post(self, blog_content, template_file_path, output_file_path):
        env = Environment(loader=FileSystemLoader("."))
        template = env.get_template(template_file_path)

        # Render the template with the provided blog content
        html_content = template.render(
            title=blog_content["title"],
            introduction=blog_content["introduction"],
            cover=blog_content["cover"],
            sections=blog_content["sections"],
            ending=blog_content["ending"],
        )

        # # Use BeautifulSoup to pretty-print the HTML
        # soup = BeautifulSoup(html_content, "html.parser")
        # formatted_html = soup.prettify()

        # Write the formatted HTML content to the output file with UTF-8 encoding
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(html_content)

    def chat_completion(
        self, prompt: str, max_words: int = 100, temperature: float = 0.2
    ) -> str:
        """
        Sends a prompt to the OpenAI API and returns the completion,
        summarizing the content if it exceeds a certain word limit.

        :param prompt: The prompt to send to the AI.
        :param max_words: The maximum number of words allowed in the response.
        :return: The AI-generated content.
        """
        openai_client = OpenAI(api_key=self.api_key)

        # Construct the prompt to communicate the desired tone as a style instruction
        prompt_with_tone = f"{self.tone} tone: {prompt}" if self.tone else prompt

        # Prepare the payload for the API request
        payload = {
            "model": "gpt-3.5-turbo",
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": self.system},
                {"role": "user", "content": prompt_with_tone},
            ],
        }

        # Send the request and get the response from OpenAI
        response = openai_client.chat.completions.create(**payload)
        content = response.choices[0].message.content.strip()

        # Update the context to include the new content
        self.context.append(content)

        # If the content is within the word limit, return the original content
        return content.replace('"', "")

    def generate_keywords(self, topic: str) -> List[str]:
        # Generate SEO-friendly keywords for a given topic
        prompt_template = config["blogger"]["blog"]["prompts"]["generate_keywords"]
        prompt = prompt_template.format(topic)
        keywords_str: str = self.chat_completion(prompt)
        self.keywords = keywords_str.split(", ")
        return self.keywords

    def incorporate_keywords(self, text: str, topic: str, max_keywords: int = 3) -> str:
        # Incorporate a set number of keywords into the text in a natural way
        used_keywords: List[str] = random.sample(
            self.keywords, min(max_keywords, len(self.keywords))
        )

        # Fetch the prompt template from the YAML configuration and format it with the topic and used keywords
        prompt_template = config["blogger"]["blog"]["prompts"]["incorporate_keywords"]
        rewrite_prompt = prompt_template.format(topic, ", ".join(used_keywords))

        # Call the chat_completion method with the formatted prompt
        rewritten_text: str = self.chat_completion(rewrite_prompt)

        # Return the rewritten text
        return rewritten_text

    def generate_title(self, topic: str) -> str:
        # Generate a title for the blog post about a given topic
        if not self.keywords:
            self.generate_keywords(topic)

        # Fetch the prompt template from the YAML configuration and format it with the topic
        prompt_template = config["blogger"]["blog"]["prompts"]["generate_title"]
        generate_title_prompt = prompt_template.format(topic)

        # Call the chat_completion method with the formatted prompt
        title: str = self.chat_completion(generate_title_prompt)

        # Return the title with quotes removed
        return title.replace('"', "")

    def generate_subtitle(self, topic: str, aspect: str = "") -> str:
        # Generate a subtitle for the blog post section.
        if not self.keywords:
            self.generate_keywords(topic)

        # Fetch the prompt template from the YAML configuration
        subtitle_prompt_template = config["blogger"]["blog"]["prompts"][
            "generate_subtitle"
        ]

        # Check if an aspect is provided and format the prompt accordingly
        if aspect:
            generate_subtitle_prompt = subtitle_prompt_template.format(topic, aspect)
        else:
            # If no aspect is provided, the template expects two placeholders but we only have one,
            # so we can pass the same topic twice.
            generate_subtitle_prompt = subtitle_prompt_template.format(topic, "")

        # Call the chat_completion method with the formatted prompt
        subtitle: str = self.chat_completion(generate_subtitle_prompt)

        # Return the subtitle with quotes removed
        return subtitle.replace('"', "")

    def generate_introduction(self, topic: str) -> str:
        # Ensure keywords are generated for SEO purposes
        if not self.keywords:
            self.generate_keywords(topic)

        # Fetch the prompt template from the YAML configuration
        introduction_prompt_template = config["blogger"]["blog"]["prompts"][
            "generate_introduction"
        ]

        # Format the prompt with the provided topic
        generate_introduction_prompt = introduction_prompt_template.format(topic)

        # Call the chat_completion method with the formatted prompt
        introduction: str = self.chat_completion(generate_introduction_prompt)

        # Incorporate keywords into the introduction for SEO optimization
        seo_optimized_introduction = self.incorporate_keywords(
            introduction, topic, max_keywords=3
        )

        return seo_optimized_introduction

    def generate_link_text(self, aspect: str) -> str:
        """
        Generate a short and concise link text for a promotional link related to a given aspect of the topic.

        :param aspect: The specific aspect of the topic to which the promotional link is related.
        :return: A string containing the short link text.
        """
        # Fetch the prompt template from the YAML configuration
        generate_link_text_prompt_template = config["blogger"]["blog"]["prompts"][
            "generate_link_text"
        ]

        # Format the prompt with the provided aspect
        generate_link_text_prompt = generate_link_text_prompt_template.format(aspect)

        # Call the chat_completion method with the formatted prompt
        link_text = self.chat_completion(generate_link_text_prompt)

        # Return the link text with any leading/trailing whitespace removed
        return link_text.strip()

    def generate_promo_context(self, aspect: str, promo_link: str) -> Dict[str, str]:
        context_prompt_template = config["blogger"]["blog"]["prompts"][
            "generate_promo_context"
        ]
        context_prompt = context_prompt_template.format(aspect, promo_link)
        promo_context = self.chat_completion(context_prompt)

        link_text_template = config["blogger"]["blog"]["prompts"]["generate_link_text"]
        link_text = self.chat_completion(link_text_template.format(aspect))

        promo_dict = {
            "content": promo_context,
            "link": promo_link,
            "link_text": link_text,
        }

        return promo_dict

    def generate_section(
        self, topic: str, aspect: str, promo_link: str = ""
    ) -> Dict[str, Union[str, List[str], Dict[str, str]]]:
        if not self.keywords:
            self.generate_keywords(topic)

        header = self.generate_subtitle(aspect)

        generate_section_prompt_template = config["blogger"]["blog"]["prompts"][
            "generate_section"
        ]
        generate_section_prompt = generate_section_prompt_template.format(topic, aspect)
        content = self.chat_completion(generate_section_prompt)
        paragraphs = content.split("\n\n")

        structured_section = {
            "header": header,
            "paragraphs": [
                self.incorporate_keywords(paragraph, topic) for paragraph in paragraphs
            ],
        }

        if promo_link:
            promo_content = self.generate_promo_context(aspect, promo_link)
            if promo_content:  # Check if promo_content is not None or empty
                structured_section["promo"] = promo_content
            else:
                print(
                    f"Warning: Promo content for aspect '{aspect}' with link '{promo_link}' is empty."
                )

        return structured_section

    def generate_main_content(
        self,
        topic: str,
        aspects: List[Union[str, Tuple[str, str]]],
        promo_on: bool = True,
    ) -> List[Dict]:
        """
        Generate the main content of the blog post divided into sections based on the given aspects.
        Aspects can be a list of strings or tuples. If it's a tuple, the second element is assumed to be the promotional link.

        :param topic: The overall topic of the blog post.
        :param aspects: A list of aspects or tuples with aspects and promo links.
        :param promo_on: A boolean to indicate if promotions should be included.
        :return: A list of structured dictionaries representing the main content sections.
        """
        structured_content_sections = (
            []
        )  # This will hold structured section data for HTML rendering

        for aspect in aspects:
            # Separate the aspect text and the promo link if it's a tuple and promo is on
            aspect_text, promo_link = (
                (aspect if isinstance(aspect, tuple) else (aspect, ""))
                if promo_on
                else (aspect, "")
            )

            # Generate a section with a promotional context if a promo link is provided, else a regular section
            section_content = self.generate_section(
                topic, aspect_text, promo_link if promo_on and promo_link else ""
            )

            # Add the structured section content to the list
            structured_content_sections.append(section_content)

        return structured_content_sections

    def generate_ending(
        self,
        main_content_sections: List[Dict[str, Any]],
        extra_links: List[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        Generate an ending statement for the blog post that includes a call to action,
        taking into account the main content of the blog and any extra promotional links.

        :param main_content_sections: The main content sections of the blog to infer the overall aspect.
        :param extra_links: Additional promotional links to be included in the ending.
        :return: A dictionary containing the ending statement and promotional links.
        """

        # Extract promotional links from the main content sections
        promo_links_list = [
            {
                "href": section.get("promo", {}).get("link", ""),
                "text": section.get("promo", {}).get("link_text", "Learn more"),
            }
            for section in main_content_sections
            if section.get("promo")
        ]

        # Add any extra links provided
        if extra_links:
            promo_links_list.extend(extra_links)

        # Determine the general aspect of the blog post for the ending statement
        aspect = (
            main_content_sections[0]["header"] if main_content_sections else "General"
        )

        # Fetch the ending prompt format from the config and fill it with the aspect
        ending_prompt = config["blogger"]["blog"]["prompts"]["generate_ending"].format(
            aspect
        )

        # Obtain the AI-generated ending content
        ending_content = self.chat_completion(ending_prompt)

        # Compile the ending structure for template rendering
        ending_structure = {"content": ending_content, "promo_links": promo_links_list}

        return ending_structure


def get_title_from_html(html_content):
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the title tag and get its text content
    title_tag = soup.find("title")
    if title_tag:
        return title_tag.get_text()
    else:
        raise ValueError("No title tag found in HTML content.")
