import os
import argparse
from typing import List


class ProjectSetup:
    def __init__(self, project_name: str, platforms: List[str]):
        self.project_name = project_name
        self.platforms = platforms

    def create_structure(self):
        os.makedirs(f"config", exist_ok=True)
        os.makedirs(f"assets/data/{self.project_name}", exist_ok=True)

        with open(f"config/{self.project_name}.yaml", "w") as file:
            file.write(f"project: {self.project_name}")

        for platform in self.platforms:
            platform_path = f"assets/data/{self.project_name}/{platform}"
            os.makedirs(f"{platform_path}/templates", exist_ok=True)
            for subfolder in ["tables", "images", "videos"]:
                os.makedirs(f"{platform_path}/{subfolder}", exist_ok=True)

    def remove_structure(self):
        os.remove(f"config/{self.project_name}.yaml")
        os.system(f"rm -rf assets/data/{self.project_name}")


def main():
    parser = argparse.ArgumentParser(description="Project Setup Script")
    parser.add_argument("--create", type=str, help="Create project structure")
    parser.add_argument("--remove", type=str, help="Remove project structure")
    parser.add_argument(
        "--platforms",
        nargs="+",
        type=str,
        default=["pinterest", "tiktok", "instagram"],
        help="List of social media platforms",
    )
    args = parser.parse_args()

    if args.create:
        project_setup = ProjectSetup(args.create, args.platforms)
        project_setup.create_structure()
    elif args.remove:
        project_setup = ProjectSetup(args.remove, args.platforms)
        project_setup.remove_structure()


if __name__ == "__main__":
    main()
