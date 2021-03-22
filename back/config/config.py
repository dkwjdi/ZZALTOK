import os
import platform

# 작업할 볼륨 또는 폴더 선정
root: str = os.path.join(os.path.splitdrive(os.getcwd())[0], "/content/") \
    if not ('gpu' in platform.node()) else os.path.abspath('content/')
image_path: str = os.path.join(root, "images/")
thumbnail_path: str = os.path.join(root, "thumbnails/")
dame_path: str = os.path.join(root, "damesource/")
first_order_model_path: str = os.path.join(root, "first-order-model/")
video_path: str = os.path.join(root, "video/")
ffmpeg_path: str = os.path.join(root, "ffmpeg/")
face_swap_model_path: str = os.path.join(root, "faceswap/")
face_swap_img_path: str = os.path.join(root, "swapimgs/")
face_swap_result_path: str = os.path.join(root, "faceswap_result/")

# 일부 전역 변수 저장
GPU_SERVER_DOMAIN: str = "ssafy4th.ddns.net"