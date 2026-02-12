import encodings
import os
import re
import shutil
import sys
from pathlib import Path

from block_markdown import markdown_to_html_node
from textnode import TextNode, TextType


def extract_title(markdown):
    if not markdown.startswith("# "):
        raise Exception(f"does not contain H1 header text extracted {markdown}")
    return markdown.strip("# ")


def copy_recursive(source_path, target_path, del_target_path=True):
    if del_target_path and Path(target_path).is_dir():
        shutil.rmtree(target_path)
        os.mkdir(target_path)
    else:
        os.mkdir(target_path)

    if not Path(source_path).is_dir() and not Path(target_path).is_dir():
        raise Exception(f"{source_path} and {target_path} do not exist")
    for item in os.listdir(source_path):
        # Directory
        if os.path.isdir(os.path.join(source_path, item)):
            # Create destination directory if needed
            new_target_dir = os.path.join(target_path, item)
            if not Path(target_path):
                os.mkdir(new_target_dir)

            new_source_dir = os.path.join(source_path, item)
            copy_recursive(new_source_dir, new_target_dir, del_target_path=False)
        else:
            source_name = os.path.join(source_path, item)
            target_name = os.path.join(target_path, item)
            shutil.copy(source_name, target_name)


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
    if not from_path.exsits() or not template_path.exsists():
        raise Exception(f"Make sure that {from_path} and {dest_path} exists")

    source_files = list_files(from_path)
    for file in source_files:
        if ".md" in file.lower():
            try:
                with Path(file).open(mode="r", encoding="utf-8") as markdown_file:
                    markdown_files.append(markdown_file)

            except Exception as e:
                raise RuntimeError(f"ERROR: Failed to load {markdown_file}: {e} file might be corrupted")

    try:
        with template_path.open(mode="r", encoding="utf-8") as template_file:
            template_html = template_file
    except Exception as e:
        raise RuntimeError(f"ERROR: Failed to load {template_file}: {e} file might be corrupted")

    for i in range(len(markdown_files)):
        if html_content.get(markdown_files[i]) is None:
            title = extract_title(markdown_files[i])
        if not title:
            raise Exception("Markdown file does not contain a Title")
        html_content[markdown_files[i]["Title"]] = title
        html_node = markdown_to_html_node(markdown_files[i])
        html_content[markdown_files[i]["html"]] = html_node.to_html()

    for file, content in html_content.items():
        output_html = re.sub(r"{{ Title }}", content["title"], template_html)
        output_html = re.sub(r"{{ Content }}", content["html"], template_html)
        html_output.append(output_html)

    if not Path(dest_path).is_dir:
        os.mkdir(dest_path)
