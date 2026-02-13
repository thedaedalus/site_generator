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
    html_content = {}
    markdown_files = []
    html_output = []
    print(f"Generating page from {from_path} to {dest_path} using {template_path} ")
    if not from_path.exists() or not template_path.exists():
        raise Exception(f"Make sure that {from_path} and {dest_path} exists")
    source_files = list_files(from_path)
    for file in source_files:
        if ".md" in file.lower():
            try:
                with open(file, mode="r", encoding="utf-8") as markdown_file:
                    markdown_files.append(markdown_file.read())

            except Exception as e:
                raise RuntimeError(f"ERROR: Failed to load {markdown_file}: {e} file might be corrupted")

    try:
        with template_path.open(mode="r", encoding="utf-8") as template_file:
            template_html = template_file.read()
    except Exception as e:
        raise RuntimeError(f"ERROR: Failed to load {template_file}: {e} file might be corrupted")

    for i in range(len(markdown_files)):
        if html_content.get(markdown_files[i]) is None:
            title = extract_title(markdown_files[i])
        if not title:
            raise Exception("Markdown file does not contain a Title")
        # print(title)
        html_content.setdefault(i, {})
        html_content[i]["title"] = title
        html_node = markdown_to_html_node(markdown_files[i])
        html_content[i]["html"] = html_node.to_html()

    for file, content in html_content.items():
        output_html = re.sub(r"{{ Title }}", content["title"], template_html)
        output_html = re.sub(r"{{ Content }}", content["html"], output_html)
        html_output.append(output_html)
    if not Path(dest_path).is_dir():
        os.mkdir(dest_path)
    with open(f"{Path(dest_path)}/index.html", mode="w", encoding="utf-8") as output:
        output.write(html_output[0])
