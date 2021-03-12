pushd %~dp0
REM 관리자 권한으로 실행하셔야 문제가 없습니다.
title JJAL Python SERVER
REM pip freeze > requirements.txt
set conda=C:\ProgramData\Miniconda3
call %conda%\Scripts\activate.bat %conda%
call conda install -c conda-forge dlib -y
REM call conda install pytorch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2 cudatoolkit=10.2 -c pytorch
call pip install -r requirements.txt
call pip install -r torch_requirements.txt -f https://download.pytorch.org/whl/cu102/torch_stable.html
call uvicorn main:app --reload --host=0.0.0.0 --port=8000