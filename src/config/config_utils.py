import yaml


def load_config(path: str) -> dict:
    with open(path, "r") as file:
        params = yaml.safe_load(file)
    return params
