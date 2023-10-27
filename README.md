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

3. Put your OPENAI API KEY in the .env file:

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
mkdir fonts
```

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
python project_processing.py create <project name>
```

3. Use the main config.yaml to set the desired parameters

```yaml
project: &project "aesthetic_destinations"

create: 20
background_dir: "data/{}/background"
topic: "..."
language: "English using basic vocabularies"
caption_style: "motivational"
social_media: "Instagram"
```

4. Handle specific specs related to each project with the config/ your project name /config.yaml if you have multiple projects.

```yaml
avoid_prompt: >
  Do not write false informations
  Do not use emojis or hastags!.
  Do not leave empty spaces between each line

example: >
  "...... \n"
  "...... \n"
  "...... \n"
```

5. Create content with create_template.py
