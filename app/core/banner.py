import json
import os

import pyfiglet


def get_app_info(file_path="data/json/app.json"):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def create_banner(app_name: str) -> str:
    return pyfiglet.figlet_format(app_name, font="slant")


def display_title(app_info: dict, language: str):
    banner = create_banner(app_info["title"])
    separator = "-" * 80
    description = (
        f"Language: \033[1m{language}\033[0m | "
        f"Build: \033[92mv{app_info['version']}\033[0m | "
        f"DEV: @{app_info['publisher']['contact']['telegram'][13:]}"
    )

    centered_banner = "\n".join([line.center(80) for line in banner.splitlines()])

    print(separator)
    print(centered_banner)
    print(separator)
    print(f"{description}".center(95))
    print(separator)


def set_window_title(app_info: dict):
    title_text = f"{app_info['title']} by @{app_info['publisher']['contact']['telegram'][13:]}"

    os_handlers = {
        'windows': lambda: os.name == 'nt',
        'other': lambda: True
    }

    title_actions = {
        'windows': lambda: os.system(f"title {title_text}"),
        'other': lambda: None
    }

    for os_key, os_func in os_handlers.items():
        if os_func():
            title_actions[os_key]()
            break
