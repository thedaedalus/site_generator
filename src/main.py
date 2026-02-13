import os
import sys
from pathlib import Path

from copystatic import copy_recursive
from generate_html import extract_title, generate_page, generate_pages_recursive, list_files


def main():
    dest_path = "docs"
    src_path = "static"
    copy_recursive(src_path, dest_path)
    from_path = "content"
    template_path = "template.html"
    if sys.argv[1]:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    generate_pages_recursive(basepath, from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
