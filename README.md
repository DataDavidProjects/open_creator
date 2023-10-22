# Open Creator

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8-blue" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-latest-green" alt="OpenAI">
  <img src="https://img.shields.io/badge/Pillow-latest-red" alt="Pillow">
</p>

## Description

Open Creator is a lightweight micro-framework designed to facilitate the creation of social media captions using OpenAI and Pillow libraries. With Open Creator, you can easily generate and customize content.

## Quick Start

### Installation

1. Clone the repository:

```bash
git clone https://github.com/DataDavidProjects/open-creator.git
```

```bash
cd open-creator
```

2. Install the requirements:

```bash
pip install -r requirements.txt
```

3. Put your OPENAI API KEY in the config.yaml file:

```bash
OPENAI_API_KEY: "your-api-key-here"
```

### Create Content

1. Create a folder named data

```bash
mkdir data/<your project name>
```

2. Create sub directories in each project you create (recommended)

```bash
mkdir data/<your project name>/background
```

```bash
mkdir data/<your project name>/tables
```

```bash
mkdir data/<your project name>/pins
```

Alternatively you can run the python file project_processing.py

```bash
mkdir data/<your project name>/pins
```

3. Use the config.yaml to set the desired parameters

4. Create content with create_template.py

```yaml
project: &project "aesthetic_destinations"

create: 20
background_dir: "data/{}/background"
topic: "Luxury and Travels"
language: "English using basic vocabularies"
caption_style: "motivational"
social_media: "Instagram"

avoid_prompt: >
  Do not write false informations
  Do not use emojis or hastags!.
  Do not leave empty spaces between each line

example: >
  "I don’t have the luxury of time to be unhappy. I have too much to do. I have too much do accomplish. Who has the time to be unhappy?. \n"
  "Time flies. It’s up to you to be the navigator. \n"
  "We wander for distraction, but we travel for fulfilment. \n"
  "Living on Earth is expensive, but it does include a free trip around the sun every year. \n"
  "It is a luxury to be understood. \n"
  "It is the ultimate luxury to combine passion and contribution. It’s also a clear path to happiness. \n"
  "Art is not a luxury, but a necessity. \n"
```
