import os
import re
import shutil
import sys
from pathlib import Path

from block_markdown import markdown_to_html_node
from copystatic import copy_recursive
from textnode import TextNode, TextType


def extract_title(markdown):
    if not markdown.startswith("# "):
        raise Exception(f"does not contain H1 header text extracted {markdown}")
    parts = markdown.split("\n\n", maxsplit=1)
    title = parts[0].lstrip("# ")
    return title


def list_files(*path):
    file_list = []
    for folder_path, _, file_names in os.walk(os.path.join(*path)):
        for file_name in file_names:
            full_path = os.path.join(folder_path, file_name)
            file_list.append(full_path)
    return file_list


def generate_page(from_path, template_path, dest_path):
    print(f"* {from_path} {template_path} -> {dest_path}")
    with open(from_path, mode="r", encoding="utf-8") as markdown_file:
        markdown_content = markdown_file.read()
    markdown_file.close()
    with open(template_path, mode="r", encoding="utf-8") as template_file:
        template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, mode="w", encoding="utf-8") as to_file:
        to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dest_file = ""
    source_files = list_files(dir_path_content)
    for file in source_files:
        dest_file = file.replace("content", dest_dir_path)
        dest_file = dest_file.replace("md", "html")
        generate_page(file, template_path, dest_file)
