import os
import subprocess
import time
import git
import urllib.request
import zipfile

# 모듈 간 충돌 방지로 인한 OMP 에러 예외처리
os.environ['KMP_DUPLICATE_LIB_OK']='True'

#작업할 볼륨 또는 폴더 선정
root = os.path.join(os.path.splitdrive(os.getcwd())[0], "/content/")
dame_path = os.path.join(root, "damesource/")
first_order_model_path = os.path.join(root, "first-order-model/")
video_path = os.path.join(root, "video/")

if not os.path.isdir(first_order_model_path):
    print("다메다메 프로젝트 클론 중")
    git.Repo.clone_from("https://github.com/AliaksandrSiarohin/first-order-model", first_order_model_path)

if not os.path.isdir(dame_path):
    print("다메다메 학습 모델 및 템플릿 다운로드 중 - 오래 걸림")
    urllib.request.urlretrieve(
        "https://github.com/KeepSOBP/dame/releases/download/damesource/damesource.zip"
        , filename= os.path.join(root, "damesource.zip") )
    with zipfile.ZipFile(os.path.join(root, "damesource.zip"), "r") as zip_ref:
        zip_ref.extractall(dame_path)
    urllib.request.urlretrieve(
        "https://github.com/KeepSOBP/dame/releases/download/damesource/bakamitai_template.mp3"
        , filename= os.path.join(dame_path, "bakamitai_template.mp3") )
    os.remove(os.path.join(root, "damesource.zip"))

# video 폴더 생성
if not os.path.isdir(video_path):
    os.makedirs(video_path, exist_ok=True)

# 필요 없는 파일 삭제
if os.path.isfile(os.path.join(root, "complete.mp4")):
  os.remove(os.path.join(root, "complete.mp4"))

# make damedane
import sys
sys.path.insert(1, first_order_model_path) # 다메다메 프로젝트 레포지토리를 추가하여 import 가능하게 조치
import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from skimage.transform import resize
import warnings
from demo import load_checkpoints, make_animation
from skimage import img_as_ubyte

def makeDamedame(uploadimage):
    filepath = convertImageToVideo(uploadimage)
    insertVideoSoundSource()

def convertImageToVideo(uploadimage):
    print("딥페이크 작업중")
    warnings.filterwarnings("ignore")

    source_image = imageio.imread(uploadimage)
    driving_video = imageio.mimread(os.path.join(dame_path, '04.mp4'))

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

    generator, kp_detector = load_checkpoints(config_path=os.path.join(first_order_model_path, 'config/vox-256.yaml'),
                                checkpoint_path=os.path.join(dame_path, 'vox-cptork.pth.tar'))
 
    # clear_output(wait=True)

    # make video
    print("영상 제작, 다운로드 진행중")
    predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True)
    filepath = os.path.join(video_path, 'original.mp4')
    imageio.mimsave(filepath, [img_as_ubyte(frame) for frame in predictions])
    return filepath
    # clear_output(wait=True)


import ffmpeg
# 영상 3배, 음원 삽입 (ffmpeg 이용)
def insertVideoSoundSource():
    # 필요 없는 파일 삭제
    if os.path.isfile(os.path.join(video_path, "complete.mp4")):
        os.remove(os.path.join(video_path, "complete.mp4"))
    print("영상 편집중")
    # !ffmpeg -i original.mp4 -r 60 -vf "setpts=(PTS-STARTPTS)/3" 3x.mp4
    (
        ffmpeg
        .input(os.path.join(video_path, 'original.mp4'))
        .output()
        .global_args('-r 60')
        .global_args('-vf "setpts=(PTS-STARTPTS)/3"')
        .global_args(os.path.join(video_path, '3x.mp4'))
        .run()
    )
    # !ffmpeg -i 3x.mp4 -i bakamitai_template.mp3 -map 0:v -map 1:a -c:v copy -shortest complete.mp4
    ffmpeg
    (
        ffmpeg
        .input(os.path.join(video_path, '3x.mp4'))
        .output('')
        .global_args('-i {}'.format(os.path.join(dame_path, "bakamitai_template.mp3")))
        .global_args('-map 0:v')
        .global_args('-map 1:a')
        .global_args('-c:v copy')
        .global_args('-shortest')
        .global_args(os.path.join(video_path, 'complete.mp4'))
        .run()
    )
    # clear_output(wait=True)

    print("영상 다운중")
    # files.download('complete.mp4')

    # os.remove(uploadimage)
    os.remove("3x.mp4")
    os.remove("original.mp4")

if __name__ == "__main__":
    makeDamedame(r"C:\content\damesource\image.png")
    #insertVideoSoundSource()