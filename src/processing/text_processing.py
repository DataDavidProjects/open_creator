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
        system: str = "You are an AI experienced in generating creative content for blogs",
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
        html_template = config["blogger"]["hmtl_template"]
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
        prompt = f"Write 5 SEO keywords for a blog post about {topic}."
        keywords_str: str = self.chat_completion(prompt)
        self.keywords = keywords_str.split(", ")
        return self.keywords

    def incorporate_keywords(self, text: str, topic: str, max_keywords: int = 3) -> str:
        # Incorporate a set number of keywords into the text in a natural way
        used_keywords: List[str] = random.sample(
            self.keywords, min(max_keywords, len(self.keywords))
        )
        rewrite_prompt: str = f"""
        Rewrite the following text to naturally include these keywords about {topic}: {', '.join(used_keywords)}.\n\n{text}
        """
        rewritten_text: str = self.chat_completion(rewrite_prompt)
        return rewritten_text

    def generate_title(self, topic: str) -> str:
        # Generate a title for the blog post about a given topic
        if not self.keywords:
            self.generate_keywords(topic)
        prompt: str = f"""Create a one line very short and engaging blog post title about {topic}."""
        title: str = self.chat_completion(prompt)
        return title.replace('"', "")

    def generate_subtitle(self, topic: str, aspect: str = "") -> str:
        """
        Generate a subtitle for the blog post section.

        :param topic: The overall topic of the blog post.
        :param aspect: The specific aspect of the topic for the section header. Optional.
        :return: A string containing the subtitle (section header).
        """
        if not self.keywords:
            self.generate_keywords(topic)

        # If an aspect is provided, use it in the prompt; otherwise, just focus on the topic
        if aspect:
            prompt = f"""
            Create a one line very short and interesting subtitle for a section of a blog post about {topic}, specifically focusing on {aspect}.
            """
        else:
            prompt = f"""
            Create a one line very short and interesting subtitle for a blog post about {topic}.
            Example output:
            Unveiling the Majestic Burj Khalifa
            """

        subtitle = self.chat_completion(prompt)
        return subtitle.replace('"', "")

    def generate_introduction(self, topic: str) -> str:
        # Generate an introduction for a blog post about a given topic
        if not self.keywords:
            self.generate_keywords(
                topic
            )  # Ensure keywords are generated for SEO purposes
        prompt: str = f"""
        Write a one line short introduction for a blog post about {topic}. Write at most 4 lines.

        Example of desired output about planning a vacation in Dubai with a luxurious style:
        We understand your dedication and hard work. You've earned the vacation of your dreams. And when it comes to such a well-deserved getaway, you undoubtedly want an environment that matches your ambitions: stylish, luxurious, and exclusive. Whether you've pondered where to find like-minded travelers or simply been curious about the top destinations and hotels favored by the VIP crowd, we've got you covered. In this article, we'll unveil the sought-after locations and accommodations where the rich and famous make their mark.
        
        """
        introduction: str = self.chat_completion(prompt)
        # Incorporate keywords into the introduction for SEO optimization
        return self.incorporate_keywords(introduction, topic, max_keywords=3)

    def generate_link_text(self, aspect: str) -> str:
        """
        Generate a short and concise link text for a promotional link related to a given aspect of the topic.

        :param aspect: The specific aspect of the topic to which the promotional link is related.
        :return: A string containing the short link text.
        """
        prompt = f"""Create a short, engaging call-to-action link text related to '{aspect}'.

        Example of output
        Deluxe Burji Khalifa Rooms: https://www.anantara.com/en/downtown-dubai/rooms/deluxe-burj-khalifa-view-room,

        """
        link_text = self.chat_completion(prompt)
        return link_text.strip()  # Ensure there's no leading/trailing whitespace

    def generate_promo_context(self, aspect: str, promo_link: str) -> Dict[str, str]:
        """
        Generate a promotional context paragraph and a short link text for the given aspect and link.

        :param aspect: The specific aspect of the topic to which the promotional link is related.
        :param promo_link: The URL for the promotional link to be included in the paragraph.
        :return: A dictionary containing the promotional content, link, and short link text.
        """
        context_prompt = f"""
            Write a friendly and informative paragraph that provides value to the reader and naturally.
            introduces a promotional link related to '{aspect}'. The link is {promo_link}. "
            Write at most 2 lines and do not write the link in the output."""
        promo_context = self.chat_completion(context_prompt)

        # Use the new method to generate a concise link text
        link_text = self.generate_link_text(aspect)

        # Structure it in a dictionary
        promo_dict = {
            "content": promo_context,
            "link": promo_link,
            "link_text": link_text,
        }

        return promo_dict

    def generate_section(
        self, topic: str, aspect: str, promo_link: str = ""
    ) -> Dict[str, Union[str, List[str], Dict[str, str]]]:
        """
        Generate a detailed section for the blog post about a given aspect of the topic.
        Optionally includes a promotional link.

        :param topic: The overall topic of the blog post.
        :param aspect: The specific aspect of the topic for the section.
        :param promo_link: The optional URL for the promotional link to be included.
        :return: A dictionary with structured section data, including the promotional content if provided.
        """
        if not self.keywords:
            self.generate_keywords(topic)

        # Generate the header and content for the section
        header = self.generate_subtitle(aspect)
        prompt = f"""Write a short detailed section for a blog post about {topic} focusing on '{aspect}'.
        You have a mandatory limit of 100 words of output text , it must be very short.
        Example of desired output with topic Dubai with aspect Skyscraper and Shopping:
        Dubai, the city of superlatives, is a playground for the world's elite. From towering skyscrapers to luxurious shopping and world-class dining, this city in the United Arab Emirates epitomizes opulence. Dubai is where dreams are made real, and it's the destination of choice for those who crave extravagance in their travels. To fully embrace the Dubai experience, consider a stay at The Palm Dubai Resort. This exquisite resort mirrors the city's grandeur, offering pristine beaches, stunning views, and impeccable service.
        """
        content = self.chat_completion(prompt)
        paragraphs = content.split(
            "\n\n"
        )  # Assuming paragraphs are separated by two newlines

        structured_section = {
            "header": header,
            "paragraphs": [
                self.incorporate_keywords(paragraph, topic) for paragraph in paragraphs
            ],
        }

        # If a promo link is provided, generate and add the promotional context
        if promo_link:
            promo_content = self.generate_promo_context(aspect, promo_link)
            promo_content["link_text"] = self.generate_link_text(
                aspect
            )  # Generate a concise link text
            structured_section["promo"] = promo_content

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
            if isinstance(aspect, tuple) and promo_on:
                # Separate the aspect text and the promo link
                aspect_text, promo_link = aspect
                # Generate a section with a promotional context
                section_content = self.generate_section(topic, aspect_text, promo_link)
            else:
                # If the aspect is not a tuple or promo is off, treat it as a regular section
                aspect_text = (
                    aspect if isinstance(aspect, str) else aspect[0]
                )  # Ensure aspect_text is a string
                section_content = self.generate_section(topic, aspect_text)

            # Add the structured section content to the list
            structured_content_sections.append(section_content)

        return structured_content_sections

    def generate_ending(
        self,
        promo_links: List[Dict[str, str]],
        main_content_sections: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate an ending statement for the blog post that includes a call to action,
        taking into account the main content of the blog to generate a relevant ending.

        :param promo_links: A list of dictionaries, each containing a promotional link and its text.
        :param main_content_sections: The main content sections of the blog to infer the overall aspect.
        :return: A dictionary containing the ending statement and promotional links.
        """

        aspect = (
            main_content_sections[0]["header"] if main_content_sections else "General"
        )

        # Generate a specific ending prompt that includes the aspect of the blog
        ending_prompt = (
            f"Write a compelling ending statement for a blog post about {aspect} "
            f"that includes a call to action for readers."
        )
        ending_content = self.chat_completion(ending_prompt)

        # Use generate_link_text to create link text for each promotional link
        promo_links_list = [
            {
                "href": link.get("link", ""),
                "text": self.generate_link_text(
                    aspect
                ),  # Use the aspect to generate relevant link text
            }
            for link in promo_links
        ]

        # Structure the ending content and promotional links for the template rendering.
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
