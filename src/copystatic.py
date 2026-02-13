import os
import re
import shutil
import sys
from pathlib import Path


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
