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
    print("다메다메 프로젝트 클론 중", end=' ')
    git.Repo.clone_from("https://github.com/AliaksandrSiarohin/first-order-model", config.first_order_model_path)
    print("done")

if not os.path.isdir(config.dame_path):
    print("다메다메 학습 모델 및 템플릿 다운로드 중 - 오래 걸림", end=' ')
    urllib.request.urlretrieve(
        "https://github.com/KeepSOBP/dame/releases/download/damesource/damesource.zip"
        , filename=os.path.join(config.root, "damesource.zip"))
    with zipfile.ZipFile(os.path.join(config.root, "damesource.zip"), "r") as zip_ref:
        zip_ref.extractall(config.dame_path)
    os.remove(os.path.join(config.root, "damesource.zip"))
    print("done")

if not os.path.exists(os.path.join(config.dame_path, "bakamitai_template.mp3")):
    print("다메다메 오디오 리소스 다운로드 중", end=' ')
    urllib.request.urlretrieve(
        "https://github.com/KeepSOBP/dame/releases/download/damesource/bakamitai_template.mp3"
        , filename=os.path.join(config.dame_path, "bakamitai_template.mp3"))
    print("done")

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
    print("다메다메 밈 작업중", end=' ')
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
    predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True)
    imageio.mimsave(outputPath, [img_as_ubyte(frame) for frame in predictions])
    print('done')
    return outputPath


def makeDamedame(uploadimagePath, output: str = os.path.join(config.video_path, 'result.mp4')):

    [filename, ext] = os.path.splitext(output)
    originPath = filename + "-origin" + ext
    subPath = filename + "-3x" + ext

    convertImageToVideo(uploadimagePath,
                        originPath)

    # 3배 빠르기로 비디오 변경, 오디오 소스 추가
    print("영상 오디오 소스 추가 및 배속 변경 중", end=' ')
    video.convert3x_faster_video(originPath, subPath)
    video.insert_audio_on_video(subPath,
                                os.path.join(config.dame_path, "bakamitai_template.mp3"),
                                output)

    if os.path.exists(originPath):
        os.remove(originPath)

    if os.path.exists(subPath):
        os.remove(subPath)
    print('done')
    return output


# print(__file__, "모듈 리소스 로드 완료")

if __name__ == "__main__":
    print("다메다메 모듈을 테스트 진행합니다.")
    print("테스트 이미지 다운로드")
    urllib.request.urlretrieve(
        "https://lab.ssafy.com/s04-ai-image-sub2/s04p22d101/uploads/95c86ac00bb9068fbaddfde923ea99f8/goo.jpg",
        r"C:\content\damesource\image.png")
    path = makeDamedame(r"C:\content\damesource\image.png")
    print("최종 결과물", path)
