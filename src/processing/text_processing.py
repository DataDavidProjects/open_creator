import random
from typing import List, Tuple, Union

import openai


class Blogger:
    """
    A class that encapsulates the functionality to generate blog posts using OpenAI's GPT model.

    Attributes:
        api_key (str): The API key for accessing OpenAI's API.
        system (str): A predefined system prompt that sets the context for the AI model.
        keywords (List[str]): A list to store the generated keywords for SEO.
        main_content_sections (List[str]): A list to store the generated main content sections for recap.

    Methods:
        chat_completion(prompt: str) -> str: Sends a prompt to the OpenAI API and returns the completion.
        generate_keywords(topic: str) -> List[str]: Generates SEO keywords for a given topic.
        incorporate_keywords(text: str, topic: str, max_keywords: int) -> str: Incorporates keywords into a given text.
        generate_title(topic: str) -> str: Generates a blog post title for a given topic.
        generate_subtitle(topic: str) -> str: Generates a blog post subtitle for a given topic.
        generate_introduction(topic: str) -> str: Generates an introduction for a blog post about a given topic.
        generate_main_content(topic: str, aspects: List[str]) -> str: Generates the main content of the blog post.
        generate_section(topic: str, aspect: str) -> str: Generates a detailed section about a given aspect of the topic.
        generate_recap(topic: str) -> str: Generates a recap paragraph summarizing the main content sections.
        generate_ending() -> str: Generates an ending statement for the blog post.
    """

    def __init__(
        self,
        api_key: str,
        system: str = "You are an AI experienced in generating creative content for blogs",
        tone: str = "",
    ) -> None:
        """
        Initializes the Blogger with an API key and an optional system prompt.

        :param api_key: The API key for OpenAI's API.
        :param system: A predefined system prompt for the AI model.
        """
        self.api_key: str = api_key
        self.system: str = system
        self.tone: str = tone
        openai.api_key = self.api_key
        self.keywords: List[str] = []
        self.main_content_sections: List[str] = []

    def chat_completion(self, prompt: str) -> str:
        # Incorporate tone into the prompt if provided
        prompt_with_tone = f"[{self.tone}] {prompt}" if self.tone else prompt
        # Send a prompt to the OpenAI API and get a response
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": self.system},
                {"role": "user", "content": prompt_with_tone},
            ],
        }
        response = openai.ChatCompletion.create(**payload)
        return response["choices"][0]["message"]["content"]

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
        rewrite_prompt: str = f"Rewrite the following text to naturally include these keywords about {topic}: {', '.join(used_keywords)}.\n\n{text}"
        rewritten_text: str = self.chat_completion(rewrite_prompt)
        return rewritten_text

    def generate_promo_context(self, aspect: str, promo_link: str) -> str:
        # Generate a promotional context paragraph for the given aspect and link
        context_prompt: str = (
            f"Write a friendly and informative paragraph that provides value to the reader and naturally "
            f"introduces a promotional link related to '{aspect}'. The link is {promo_link}. "
            f"The style should be engaging and encourage the reader to learn more without a direct sales pitch."
        )
        promo_context: str = self.chat_completion(context_prompt)
        return promo_context

    def generate_title(self, topic: str) -> str:
        # Generate a title for the blog post about a given topic
        if not self.keywords:
            self.generate_keywords(topic)
        prompt: str = f"Create an engaging blog post title about {topic}."
        title: str = self.chat_completion(prompt)
        return self.incorporate_keywords(title, topic, max_keywords=1)

    def generate_subtitle(self, topic: str) -> str:
        # Generate a subtitle for the blog post
        if not self.keywords:
            self.generate_keywords(topic)
        prompt: str = f"Create an interesting subtitle for a blog post about {topic}."
        subtitle: str = self.chat_completion(prompt)
        return self.incorporate_keywords(subtitle, topic, max_keywords=2)

    def generate_introduction(self, topic: str) -> str:
        # Generate an introduction for a blog post about a given topic
        if not self.keywords:
            self.generate_keywords(
                topic
            )  # Ensure keywords are generated for SEO purposes
        prompt: str = f"Write an introduction for a blog post about {topic}."
        introduction: str = self.chat_completion(prompt)
        # Incorporate keywords into the introduction for SEO optimization
        return self.incorporate_keywords(introduction, topic, max_keywords=3)

    def generate_main_content(
        self,
        topic: str,
        aspects: List[Union[str, Tuple[str, str]]],
        promo_on: bool = True,
    ) -> str:
        # Generate the main content of the blog post divided into sections based on the given aspects
        # aspects can be a list of strings or tuples. If it's a tuple, the second element is assumed to be the promotional link.
        self.main_content_sections = []  # Resetting for a new blog post
        for aspect in aspects:
            aspect_text = aspect
            promo_context = ""
            if isinstance(aspect, tuple) and promo_on:
                # If the aspect is a tuple and promotions are turned on, separate the text and the promo link
                aspect_text, promo_link = aspect
                promo_context = self.generate_promo_context(aspect_text, promo_link)

            # Generate a regular section
            section = self.generate_section(topic, aspect_text)
            # Append promotional context if there is one
            section = f"{section} {promo_context}" if promo_context else section
            self.main_content_sections.append(section)

        return "\n\n".join(self.main_content_sections)

    def generate_section(self, topic: str, aspect: str) -> str:
        # Generate a detailed section for the blog post about a given aspect of the topic
        if not self.keywords:
            self.generate_keywords(
                topic
            )  # Ensure keywords are generated for SEO purposes
        prompt: str = f"Write a detailed section for a blog post about {topic} focusing on '{aspect}'."
        section: str = self.chat_completion(prompt)
        # Incorporate keywords into the section for SEO optimization
        return self.incorporate_keywords(section, topic)

    def generate_recap(self, topic: str) -> str:
        # Generate a recap that summarizes the main content sections of the blog post
        if not self.main_content_sections:
            raise ValueError(
                "No content sections to summarize. Generate main content first."
            )

        # Construct a prompt to summarize the sections
        summary_prompt: str = (
            "Summarize the key points from the following sections:\n\n"
            + "\n\n".join(self.main_content_sections)
        )
        # Call the API to generate a summary based on the content sections
        recap: str = self.chat_completion(summary_prompt)
        # Incorporate keywords into the recap for SEO optimization
        return self.incorporate_keywords(recap, topic, max_keywords=3)

    def generate_ending(self) -> str:
        # Generate an ending statement for the blog post, typically including a call to action
        ending_prompt: str = "Write a compelling ending statement for a blog post that includes a call to action for readers."
        # Call the API to generate the ending based on the prompt
        ending: str = self.chat_completion(ending_prompt)
        # There's no need to incorporate keywords in the ending as it's a call to action, but you can if it's relevant
        return ending
