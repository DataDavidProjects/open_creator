from setuptools import find_packages, setup

setup(
    name="open_creator",
    version="0.1.0",
    description="A microframework for creating social media content",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="DataProjects",
    author_email="davis.dataprojects@gmail.com",
    url="https://github.com/DavisDataProjects/open_creator",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "Pillow",
        "PyYAML",
        "openai",
        "numpy",
        "python-dotenv",
    ],
)
