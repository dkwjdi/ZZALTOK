# 요즘짤생성기

딥러닝을 접목한 요소로 딥러닝이라는 학문에 보다 친근감 있게 접근할 수 있는 재미를 위한 요소 개발에 중점을 둔 프로젝트

# 팀원소개

### 프론트

<img src="/uploads/95c86ac00bb9068fbaddfde923ea99f8/goo.jpg" width="100px" height="100px">&emsp;
<img src="/uploads/ba2a3448a0c37d1793d6c6ee48c57055/4.jpg" width="100px" height="100px">
<br>&emsp;강구원 &emsp;&emsp;&emsp;&emsp;&emsp;정준영

### 백엔드

<img src="/uploads/7640898ee20c5daec513d93820395bf8/2.jpg" width="100px" height="100px">&emsp;
<img src="/uploads/102c25d71feaf1951631d7100c99c180/3.jpg" width="100px" height="100px">
<br>&emsp;현진혁 &emsp;&emsp;&emsp;&emsp;&emsp;곽충섭

### 서버

<img src="/uploads/caba213988a96f88a9509cf2d29a3b9a/5.png" width="100px" height="100px">
<br>&emsp;박정환

## 설치방법

Jenkins 파이프라인을 위한 스크립트를 사용합니다. 해당 문서를 확인해주세요.

### Windows

> #### 서버
>
> 1. [미니콘다](https://docs.conda.io/en/latest/miniconda.html) 설치
> 2. [CUDA 10.1](https://developer.nvidia.com/cuda-10.1-download-archive-base) 설치
> 3. .\back\install.bat 실행
> 4. .\back\run.bat 실행

> #### 클라이언트(Vue.js)
>
> ```cmd
> cd .\front
> npm install
> npm build
> ```

### Linux

`***required docker, jenkins***`

- Defining a [Pipeline in SCM](https://www.jenkins.io/doc/book/pipeline/getting-started#defining-a-pipeline-in-scm),
  a Jenkinsfile is a text file that contains the definition of a Jenkins Pipeline and is checked into source control. Using `Jenkinsfile`.

## 기능소개

### 주요 3기능 - 얼굴 체인지, 다메다메 영상, 나만의 배경 기능

<img src="/uploads/4676e702c6057b830a69b737c6bd6153/1.gif" width="45%" height="400"></img>
<img src="/uploads/32af7c3d15bb992614cf69c004f429e3/2.gif" width="45%" height="400"></img>
<img src="/uploads/6f2cb9d337511a82cf8d02525fba5e73/3.gif" width="45%" height="400"></img>
<img src="/uploads/6d568150ae68cff9155e4a05237edc5c/4.gif" width="45%" height="400"></img>

### 짤 공유 기능, 게시글 댓글 쓰기 기능

<img src="/uploads/2780bc02d80e99e51493a4c5927bc05e/5.gif" width="45%"></img>
<img src="/uploads/d8b79ac593b0ec3472fc7fa349167063/6.gif" width="45%"></img>

## 기여

Pull & Merge Request 요청을 환영합니다.

주요 변경 사항은 먼저 문제를 열어 변경하고자 하는 사항에 대해 논의하십시오.

(필요에 따라 테스트를 업데이트하십시오.)

## License

[MIT](https://choosealicense.com/licenses/mit/)
