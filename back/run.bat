pushd %~dp0
REM 관리자 권한으로 실행하셔야 문제가 없습니다.
title JJAL Python SERVER
REM pip freeze > requirements.txt
set conda=C:\ProgramData\Miniconda3
call %conda%\Scripts\activate.bat %conda%
call conda install -c conda-forge dlib -y
call pip install -r requirements.txt
call uvicorn main:app --reload --host=0.0.0.0 --port=8000