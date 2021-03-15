import os

# 작업할 볼륨 또는 폴더 선정
root: str = os.path.join(os.path.splitdrive(os.getcwd())[0], "/content/")
image_path: str = os.path.join(root, "images/")
dame_path: str = os.path.join(root, "damesource/")
first_order_model_path: str = os.path.join(root, "first-order-model/")
video_path: str = os.path.join(root, "video/")
ffmpeg_path: str = os.path.join(root, "ffmpeg/")
