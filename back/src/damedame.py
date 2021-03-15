import os
import platform
import subprocess
import time
import git
import urllib.request
import zipfile
import stat
from config import config
from utils import video

if not os.path.isdir(config.first_order_model_path):
    print("다메다메 프로젝트 클론 중")
    git.Repo.clone_from("https://github.com/AliaksandrSiarohin/first-order-model", config.first_order_model_path)

if not os.path.isdir(config.dame_path):
    print("다메다메 학습 모델 및 템플릿 다운로드 중 - 오래 걸림")
    urllib.request.urlretrieve(
        "https://github.com/KeepSOBP/dame/releases/download/damesource/damesource.zip"
        , filename=os.path.join(config.video_path, "damesource.zip"))
    with zipfile.ZipFile(os.path.join(config.root, "damesource.zip"), "r") as zip_ref:
        zip_ref.extractall(config.dame_path)
    urllib.request.urlretrieve(
        "https://github.com/KeepSOBP/dame/releases/download/damesource/bakamitai_template.mp3"
        , filename=os.path.join(config.dame_path, "bakamitai_template.mp3"))
    os.remove(os.path.join(config.root, "damesource.zip"))

# # 필요 없는 파일 삭제
# if os.path.isfile(os.path.join(config.root, "complete.mp4")):
#     os.remove(os.path.join(config.root, "complete.mp4"))

# make damedane
import sys

sys.path.insert(1, config.first_order_model_path)  # 다메다메 프로젝트 레포지토리를 추가하여 import 가능하게 조치
import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.transform import resize
import warnings
from demo import load_checkpoints, make_animation
from skimage import img_as_ubyte

import utils.video


def convertImageToVideo(uploadimage, outputPath):
    print("딥페이크 작업중")
    warnings.filterwarnings("ignore")

    source_image = imageio.imread(uploadimage)
    driving_video = imageio.mimread(os.path.join(config.dame_path, '04.mp4'))

    source_image = resize(source_image, (256, 256))[..., :3]
    driving_video = [resize(frame, (256, 256))[..., :3] for frame in driving_video]

    def display(source, driving, generated=None):
        fig = plt.figure(figsize=(8 + 4 * (generated is not None), 6))

        ims = []
        for i in range(len(driving)):
            cols = [source]
            cols.append(driving[i])
            if generated is not None:
                cols.append(generated[i])
            im = plt.imshow(np.concatenate(cols, axis=1), animated=True)
            plt.axis('off')
            ims.append([im])

        ani = animation.ArtistAnimation(fig, ims, interval=50, repeat_delay=1000)
        plt.close()
        return ani

    generator, kp_detector = load_checkpoints(
        config_path=os.path.join(config.first_order_model_path, 'config/vox-256.yaml'),
        checkpoint_path=os.path.join(config.dame_path, 'vox-cpk.pth.tar'))

    # make video
    print("영상 제작 진행 중")
    predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True)
    imageio.mimsave(outputPath, [img_as_ubyte(frame) for frame in predictions])
    return outputPath


def makeDamedame(uploadimagePath, output: str = os.path.join(config.video_path, 'original.mp4')):
    convertImageToVideo(uploadimagePath,
                        output)
    [filename, ext] = os.path.splitext(output)
    print("filename", filename)
    print("ext", ext)
    subPath = filename + "-3x" + ext
    resultPath = filename + "-complete" + ext
    # 3배 빠르기로 비디오 변경, 오디오 소스 추가
    print("영상 오디오 소스 추가 및 배속 변경 중")
    video.convert3xFasterVideo(output, subPath)
    video.insertAudioOnVideo(subPath,
                             os.path.join(config.dame_path, "bakamitai_template.mp3"),
                             resultPath)

    if os.path.exists(output):
        os.remove(output)
    if os.path.exists(subPath):
        os.remove(subPath)
    return resultPath


if __name__ == "__main__":
    print("다메다메 모듈을 테스트 진행합니다.")
    print("테스트 이미지 다운로드")
    urllib.request.urlretrieve(
        "https://lab.ssafy.com/s04-ai-image-sub2/s04p22d101/uploads/95c86ac00bb9068fbaddfde923ea99f8/goo.jpg",
        r"C:\content\damesource\image.png")
    path = makeDamedame(r"C:\content\damesource\image.png")
    print("최종 결과물", path)
