import os

def make_dir(path: str):
    if not os.path.exists(path):
        os.mkdir(path)