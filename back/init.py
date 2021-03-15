import os
from config import config


def init():
    # video 폴더 생성
    if not os.path.isdir(config.video_path):
        os.makedirs(config.video_path, exist_ok=True)

    # images 폴더 생성
    if not os.path.isdir(config.image_path):
        os.makedirs(config.image_path, exist_ok=True)
