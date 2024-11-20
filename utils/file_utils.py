import os
import shutil
from typing import Optional

def ensure_directory(path: str):
    """确保目录存在"""
    if not os.path.exists(path):
        os.makedirs(path)

def read_file(path: str, encoding: str = 'utf-8') -> str:
    """读取文件内容"""
    with open(path, 'r', encoding=encoding) as f:
        return f.read()

def write_file(path: str, content: str, encoding: str = 'utf-8'):
    """写入文件内容"""
    ensure_directory(os.path.dirname(path))
    with open(path, 'w', encoding=encoding) as f:
        f.write(content)

def copy_file(src: str, dst: str):
    """复制文件"""
    ensure_directory(os.path.dirname(dst))
    shutil.copy2(src, dst)

def delete_file(path: str):
    """删除文件"""
    if os.path.exists(path):
        os.remove(path)

def list_files(directory: str, extension: Optional[str] = None):
    """列出目录中的文件"""
    files = []
    for file in os.listdir(directory):
        if extension is None or file.endswith(extension):
            files.append(os.path.join(directory, file))
    return files 