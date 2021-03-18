import os
import platform
import subprocess
import urllib.request
import zipfile
import stat

from config import config

# ffmpeg 파일 다운로드
if not os.path.isdir(config.ffmpeg_path):
    urllib.request.urlretrieve(
        "http://kumoh.synology.me/ffmpeg.zip"
        , filename=os.path.join(config.root, "ffmpeg.zip"))
    with zipfile.ZipFile(os.path.join(config.root, "ffmpeg.zip"), "r") as zip_ref:
        zip_ref.extractall(config.ffmpeg_path)
    if platform.system() == "Windows":  # 윈도우인 경우 linux 실행 파일을 삭제
        os.remove(os.path.join(config.ffmpeg_path, "ffmpeg"))
    else:  # 리눅스인 경우 실행 권한 추가
        st = os.stat(os.path.join(config.ffmpeg_path, "ffmpeg"))
        os.chmod(os.path.join(config.ffmpeg_path, "ffmpeg"), st.st_mode | stat.S_IEXEC)

if os.path.isfile(os.path.join(config.root, "ffmpeg.zip")):
    os.remove(os.path.join(config.root, "ffmpeg.zip"))

def convert3xFasterVideo(inputPath:str, ouputPath:str):
    # !ffmpeg -i original.mp4 -r 60 -vf "setpts=(PTS-STARTPTS)/3" 3x.mp4
    cmd = '{} -i {} -r 60 -vf "setpts=(PTS-STARTPTS)/3" {} -y'.format(
        os.path.join(config.ffmpeg_path, 'ffmpeg'),
        inputPath,
        ouputPath
    )
    subprocess.Popen(cmd).wait()

def insertAudioOnVideo(inputVideoPath: str, inputAudioPath: str, outputPath: str):
    # !ffmpeg -i 3x.mp4 -i bakamitai_template.mp3 -map 0:v -map 1:a -c:v copy -shortest complete.mp4
    cmd = '{} -i {} -i {} -map 0:v -map 1:a -c:v copy -shortest {} -y'.format(
        os.path.join(config.ffmpeg_path, 'ffmpeg'),
        inputVideoPath,
        inputAudioPath,
        outputPath
    )
    subprocess.Popen(cmd).wait()

def createVideoThumbnail(inputVideoPath, outputImagePath):
    if os.path.splitext(outputImagePath)[-1].lower() != '.png':
        raise Exception('Only png files are allowed for output')
    # !ffmpeg.exe -i twice.mp4 -vcodec png -vframes 1 -vf thumbnail=100 result.png
    cmd = "{} -i {} -vcodec png -vframes 1 -vf thumbnail=100 {}".format(
        os.path.join(config.ffmpeg_path, 'ffmpeg'),
        inputVideoPath,
        outputImagePath
    )
    subprocess.Popen(cmd).wait()
