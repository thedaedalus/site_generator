import os
from pathlib import Path

from copystatic import copy_recursive
from generate_html import extract_title, generate_page, list_files


def main():
    dest_path = "public"
    src_path = "static"
    copy_recursive(src_path, dest_path)
    from_path = Path("content")
    template_path = Path("template.html")

    generate_page(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
