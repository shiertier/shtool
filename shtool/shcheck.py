#shcheck.py
import os

def is_directory(path):
    if not os.path.isdir(path):
        raise ValueError(f"无效的目录路径: {path}")
        exit()
    os.makedirs(output_directory, exist_ok=True)

def is_file(path):
    if not os.path.isfile(path):
        raise ValueError(f"无效的文件路径: {path}")
        exit()

def is_zip_file(path):
    if not path.endswith('.zip'):
        raise ValueError(f"无效的 zip 文件路径: {path}")
        exit()
