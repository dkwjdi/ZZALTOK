import os
import platform
import subprocess
import time
import git
import urllib.request
import zipfile
import stat

#작업할 볼륨 또는 폴더 선정
root = os.path.join(os.path.splitdrive(os.getcwd())[0], "/content/")
dame_path = os.path.join(root, "damesource/")
first_order_model_path = os.path.join(root, "first-order-model/")
video_path = os.path.join(root, "video/")
ffmpeg_path = os.path.join(root, "ffmpeg/")

if not os.path.isdir(first_order_model_path):
    print("다메다메 프로젝트 클론 중")
    git.Repo.clone_from("https://github.com/AliaksandrSiarohin/first-order-model", first_order_model_path)

if not os.path.isdir(dame_path):
    print("다메다메 학습 모델 및 템플릿 다운로드 중 - 오래 걸림")
    urllib.request.urlretrieve(
        "https://github.com/KeepSOBP/dame/releases/download/damesource/damesource.zip"
        , filename= os.path.join(video_path, "damesource.zip") )
    with zipfile.ZipFile(os.path.join(root, "damesource.zip"), "r") as zip_ref:
        zip_ref.extractall(dame_path)
    urllib.request.urlretrieve(
        "https://github.com/KeepSOBP/dame/releases/download/damesource/bakamitai_template.mp3"
        , filename= os.path.join(dame_path, "bakamitai_template.mp3") )
    os.remove(os.path.join(root, "damesource.zip"))

# video 폴더 생성
if not os.path.isdir(video_path):
    os.makedirs(video_path, exist_ok=True)

# ffmpeg 파일 다운로드
if not os.path.isdir(ffmpeg_path):
    urllib.request.urlretrieve(
        "http://kumoh.synology.me/ffmpeg.zip"
        , filename= os.path.join(root, "ffmpeg.zip") )
    with zipfile.ZipFile(os.path.join(root, "ffmpeg.zip"), "r") as zip_ref:
        zip_ref.extractall(ffmpeg_path)
    if platform.system() == "Windows": #윈도우인 경우 linux 실행 파일을 삭제
        os.remove(os.path.join(ffmpeg_path, "ffmpeg"))
    else: # 리눅스인 경우 실행 권한 추가
        st = os.stat(os.path.join(ffmpeg_path, "ffmpeg"))
        os.chmod(os.path.join(ffmpeg_path, "ffmpeg"), st.st_mode | stat.S_IEXEC)

# 필요 없는 파일 삭제
if os.path.isfile(os.path.join(root, "complete.mp4")):
  os.remove(os.path.join(root, "complete.mp4"))

if os.path.isfile(os.path.join(root, "ffmpeg.zip")):
    os.remove(os.path.join(root, "ffmpeg.zip"))

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
                                checkpoint_path=os.path.join(dame_path, 'vox-cpk.pth.tar'))


    # make video
    print("영상 제작, 다운로드 진행중")
    predictions = make_animation(source_image, driving_video, generator, kp_detector, relative=True)
    filepath = os.path.join(video_path, 'original.mp4')
    imageio.mimsave(filepath, [img_as_ubyte(frame) for frame in predictions])
    return filepath


# 영상 3배, 음원 삽입 (ffmpeg 이용)
def insertVideoSoundSource():
    # 필요 없는 파일 삭제
    if os.path.isfile(os.path.join(video_path, "complete.mp4")):
        os.remove(os.path.join(video_path, "complete.mp4"))
    print("영상 편집중")
    # !ffmpeg -i original.mp4 -r 60 -vf "setpts=(PTS-STARTPTS)/3" 3x.mp4
    cmd = '{} -i {} -r 60 -vf "setpts=(PTS-STARTPTS)/3" {} -y'.format(
        os.path.join(ffmpeg_path, 'ffmpeg'),
        os.path.join(video_path, 'original.mp4'),
        os.path.join(video_path, '3x.mp4')
    )
    subprocess.Popen(cmd).wait()
    # !ffmpeg -i 3x.mp4 -i bakamitai_template.mp3 -map 0:v -map 1:a -c:v copy -shortest complete.mp4
    cmd = '{} -i {} -i {} -map 0:v -map 1:a -c:v copy -shortest {} -y'.format(
        os.path.join(ffmpeg_path, 'ffmpeg'),
        os.path.join(video_path, '3x.mp4'),
        os.path.join(dame_path, "bakamitai_template.mp3"),
        os.path.join(video_path, 'complete.mp4')
    )
    subprocess.Popen(cmd).wait()
    print("다메다메 영상 제작 완료")

    # os.remove(uploadimage)
    # os.remove("3x.mp4")
    # os.remove("original.mp4")

if __name__ == "__main__":
    makeDamedame(r"C:\content\damesource\image.png")
    #insertVideoSoundSource()