import os
from pathlib import Path

from generate_html import copy_recursive, extract_title, list_files


def main():
    # dest_path = "public"
    # src_path = "static"
    # copy_recursive(src_path, dest_path)

    path = "content"
    files = list_files(path)
    for file in files:
        if ".md" in file:
            print(file)

    # print(list_files()


if __name__ == "__main__":
    main()
