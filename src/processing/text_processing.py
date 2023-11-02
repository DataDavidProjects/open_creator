import random

import openai

api_key = "***"


class Blogger:
    def __init__(
        self, api_key, system="You are an expert Social Media Manager for Pinterest"
    ):
        self.api_key = api_key
        self.system = system
        openai.api_key = self.api_key
        self.keywords = []  # To store the generated keywords

    def chat_completion(self, prompt):
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": self.system},
                {"role": "user", "content": prompt},
            ],
        }
        response = openai.ChatCompletion.create(**payload)
        return response["choices"][0]["message"]["content"]

    def generate_keywords(self, topic):
        prompt = f"What are some SEO keywords for a blog post about {topic}?"
        keywords_str = self.chat_completion(prompt)
        self.keywords = keywords_str.split(
            ", "
        )  # Assuming the API returns keywords separated by commas
        return self.keywords

    def incorporate_keywords(self, text, max_keywords=3):
        # Incorporates a maximum of `max_keywords` into the text.
        used_keywords = random.sample(
            self.keywords, min(max_keywords, len(self.keywords))
        )
        return f"{text} {' '.join(used_keywords)}"

    def generate_title(self, topic):
        if not self.keywords:
            self.generate_keywords(topic)
        prompt = f"Create an engaging blog post title about {topic}"
        title = self.chat_completion(prompt)
        return self.incorporate_keywords(
            title, max_keywords=1
        )  # Use fewer keywords in titles for clarity

    def generate_subtitle(self, topic):
        if not self.keywords:
            self.generate_keywords(topic)
        prompt = f"Create an interesting subtitle for a blog post about {topic}"
        subtitle = self.chat_completion(prompt)
        return self.incorporate_keywords(subtitle, max_keywords=2)

    def generate_section(self, topic, section_title):
        if not self.keywords:
            self.generate_keywords(topic)
        prompt = f"Write a detailed section for a blog post about {topic} titled '{section_title}'"
        section = self.chat_completion(prompt)
        return self.incorporate_keywords(section)  # Use more keywords in sections

    def generate_section_title(self, topic):
        if not self.keywords:
            self.generate_keywords(topic)
        # Use a keyword in the section title for SEO
        keyword_for_title = random.choice(self.keywords)
        prompt = f"Create a compelling section title for a blog post about {topic} that includes the keyword '{keyword_for_title}'"
        return self.chat_completion(prompt)

    def generate_conclusion(self, topic):
        # We assume that the conclusion will wrap up the content presented in the blog post.
        if not self.keywords:
            self.generate_keywords(topic)
        prompt = f"Summarize the key points of a blog post about {topic} in a concluding paragraph without using bullet points."
        conclusion = self.chat_completion(prompt)
        return self.incorporate_keywords(
            conclusion
        )  # Incorporate keywords into the conclusion


# Usage example:

blogger = Blogger(api_key)

topic = "Pinterest marketing"

# Generate parts of the blog post
title = blogger.generate_title(topic)
subtitle = blogger.generate_subtitle(topic)
section_titles_and_content = [
    (blogger.generate_section_title(topic), blogger.generate_section(topic, title))
    for _ in range(3)
]
conclusion = blogger.generate_conclusion(topic)

# Output the blog post
print(f"Title: {title}\n")
print(f"Subtitle: {subtitle}\n")
for i, (section_title, section_content) in enumerate(section_titles_and_content, 1):
    print(f"Section {i} Title: {section_title}\n")
    print(f"{section_content}\n")
print("Conclusion:\n")
print(conclusion)
