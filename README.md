# Open Creator

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8-blue" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-latest-green" alt="OpenAI">
  <img src="https://img.shields.io/badge/Pillow-latest-red" alt="Pillow">
</p>

## Description

Open Creator is a lightweight micro-framework designed to facilitate the creation of social media captions using OpenAI and Pillow libraries. With Open Creator, you can easily generate and customize content.

### Project Setup

The `project_setup.py` script is provided to help you initialize a new project with the necessary directory structure. This script creates a configuration file and organizes your project's assets into separate directories for each social media platform.

#### Usage

1. **Creating a New Project**:

   - Navigate to the directory containing `project_setup.py`.
   - Run the following command in your terminal:
     ```bash
     python project_setup.py --create <project_name> --platforms <platform1> <platform2> ...
     ```
   - Replace `<project_name>` with the name of your project (e.g., `aesthetic_destinations`), and `<platform1> <platform2> ...` with the social media platforms you are targeting (e.g., `pinterest tiktok instagram`).

   Example:

   ```bash
   python project_setup.py --create aesthetic_destinations --platforms pinterest tiktok instagram
   ```

2. **Removing a Project**:

   - If you need to remove a project and its associated directories, run the following command:
     ```bash
     python project_setup.py --remove <project_name>
     ```
   - Replace `<project_name>` with the name of the project you wish to remove.

   Example:

   ```bash
   python project_setup.py --remove aesthetic_destinations
   ```

This script simplifies the setup and teardown of your project environment, allowing you to focus on content creation.
