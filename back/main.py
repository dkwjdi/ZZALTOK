import os
import uuid

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from utils import db, url, video
from config import config
from init import init
from src import damedame as dame
from src import startfaceswap as faceswap
from PIL import Image

init()

app = FastAPI()

### 여기부터 메인기능 시작 ###

#  S04P22D101-54	백엔드 RESTful API 프로토콜 / 가짜 격언 생성 기능에서 얼굴 합성 딥페이크
# input : origin위인 사진, target합성할 얼굴 사진
# output : 합성된 사진 (위인 사진 기준)
@app.post("/api/v1/deepfake", name="얼굴 합성 딥페이크 서비스")
async def createDeepFakeImage(origin: UploadFile = File(...), target: UploadFile = File(...)):
    content_origin = await origin.read()
    ext = origin.filename[origin.filename.rfind('.'):]
    origin.filename = str(uuid.uuid4()).replace('-', '') + ext

    content_target = await target.read()
    ext = target.filename[target.filename.rfind('.'):]
    target.filename = str(uuid.uuid4()).replace('-', '') + ext

    origin_input = os.path.join(config.face_swap_img_path, origin.filename)
    target_input = os.path.join(config.face_swap_img_path, target.filename)
    output = os.path.join(config.face_swap_result_path, str(uuid.uuid4()).replace('-', '') + ".png")

    print("origininput:", origin_input)
    print("target_input:", target_input)

    with open(origin_input, "wb") as fp:
        fp.write(content_origin)
    with open(target_input, "wb") as fp:
        fp.write(content_target)

    faceswap.makedeepface(uploadoriginimagePath=origin_input, uploadtargetimagePath=target_input, output=output)
    return {"url": url.convertPathToURL(output, baseUrl="/api/v1/content/")}


#  S04P22D101-55	백엔드 RESTful API 프로토콜 / 다메다메 짤 생성
# input : 합성할 얼굴 사진
# output : 합성된 동영상
@app.post("/api/v1/damedame", name="다메다메 짤 생성 서비스")
async def createDameMemeVideo(image: UploadFile = File(...)):
        contents = await image.read()
        image.filename = image.filename.replace(' ', '')
        input = os.path.join(config.image_path, image.filename)
        output = os.path.join(config.video_path, str(uuid.uuid4()).replace('-', '') + ".mp4")
        with open(input, "wb") as fp:
            fp.write(contents)
        print("input:",input)
        dame.makeDamedame(uploadimagePath=input, output=output)
        return {"url": url.convertPathToURL(output, baseUrl="/api/v1/content/")}


#  S04P22D101-56	백엔드 RESTful API 프로토콜 / 동영상 배경 삭제 및 배경 변경
# input : 동영상, 배경사진
# output : 합성된 동영상
@app.post("/api/v1/removeBg", name="동영상 배경 변경 서비스")
async def removeBackGroundOnVideo(video: UploadFile = File(...), image: UploadFile = File(...)):
    pass

@app.get("/api/v1/content/{rest_of_path:path}", name="파일 가져오기")
async def serveUploadFile(rest_of_path: str, download: bool = False):
    print("다운로드")
    filepath = os.path.join(config.root, rest_of_path)
    if os.path.exists(filepath):
        if download:
            return FileResponse(filepath, media_type="application/octet-stream")
        return FileResponse(filepath)
    else:
        return JSONResponse(status_code=400, content={"message": "존재하지 않는 파일입니다."})

# S04P22D101-106     최근 게시글 조회에 필요한 썸네일 생성
# input : 만들어진 output의 파일 경로, type(0 - 이미지, 1 - 동영상)
# output : 썸네일(이름은 board_no.jpg)
@app.get("/api/v1/thumbnails/{rest_of_path:path}", name="썸네일 호출 및 만들기")
async def makeThumbnails(
        rest_of_path: str,
        board_no: int,
        type: int,
):
    print("Thumbnails 제작 및 호출")
    filepath = os.path.join(config.root, rest_of_path)
    # Image
    if type == 0:
        try:
            imagepath = os.path.join(config.thumbnail_path, str(board_no) + ".png")
            print(imagepath)
            if os.path.isfile(imagepath) is False:
                image = Image.open(filepath)
                image_resize = image.resize((240, 136))
                image_resize.save(imagepath)
            return FileResponse(imagepath)
        except IOError:
            return JSONResponse(status_code=400, content={"message": "썸네일 제작중 에러 발생"})

    # Video
    else:
        output = os.path.join(config.thumbnail_path, str(board_no) + ".png")
        if os.path.isfile(output) is False:
            video.createVideoThumbnail(inputVideoPath=filepath, outputImagePath=output)
            image = Image.open(output)
            image_resize = image.resize((240, 136))
            image_resize.save(output)

        return FileResponse(output)


### 여기까지 메인기능 종료 ###


### 여기부터 게시글 기능 시작 ###

#  S04P22D101-63	백엔드 RESTful API 프로토콜 / 최근 게시글들 조회(추천순 반영)
@app.get("/api/v1/board", name="전체 게시글 조회(24시간 내, 추천순)")
async def findAllBoardOnDay():
    result = await db.findAllBoardOnDay()
    # return JSONResponse(status_code=200, content={"items":result})
    if result is None:
        return JSONResponse(status_code=400, content={"message": "게시글 조회에 실패하였습니다."})
    return {"items": result}


#  S04P22D101-64     백엔드 RESTful API 프로토콜 / 게시글 상세 조회
@app.get("/api/v1/board/detail/{board_no}", name="게시글 상세 조회")
async def findBoardDetailByBoardNo(board_no: int):
    result = await db.findBoardDetailByBoardNo(board_no)
    if result is None:
        return JSONResponse(status_code=400, content={"message": "존재하지 않는 게시글입니다."})
    return result


#  S04P22D101-57	백엔드 RESTful API 프로토콜 / 게시글 작성(공유)
# input : content(게시글 내용), content_type(게시글 내용 - 구분용), nickname(익명 닉네임), password(비밀번호)
# output : 게시글 작성 성공 유무
@app.post("/api/v1/board/write", name="게시글 작성")
async def writeBoard(
        title: str, content: str, content_type: str, nickname: str, password: str, request: Request
):
    ip = request.client.host
    board_info = {
        "title": title,
        "content": content,
        "content_type": content_type,
        "nickname": nickname,
        "password": password,
        "ip": ip
    }
    result = await db.writeBoard(board_info)
    if result is None:
        return JSONResponse(status_code=400, content={"message": "게시물 작성에 실패했습니다."})


    return result


#  S04P22D101-67     백엔드 RESTful API 프로토콜 / 게시글 수정
# output : 게시글 수정 성공 유무
@app.post("/api/v1/board/{board_no}", name="게시글 수정")
async def editBoard(
        board_no: int, title: str, content: str, content_type: str, nickname: str, password: str, request: Request
):
    ip = request.client.host
    board_info = {
        "title": title,
        "content": content,
        "content_type": content_type,
        "nickname": nickname,
        "password": password,
        "ip": ip,
        "board_no": board_no
    }
    res_check = await checkBoard(board_no, password)

    if res_check['result'] is None:
        return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})

    if res_check['result']:
        result = await db.editBoard(board_info)
        if result is None:
            return JSONResponse(status_code=400, content={"message": "게시물 수정에 실패했습니다."})
        return result
    else:
        return JSONResponse(status_code=400, content={"message": "비밀번호가 일치하지 않습니다."})


#  S04P22D101-60	백엔드 RESTful API 프로토콜 / 게시글 삭제
# input : board_no(보드번호), password(비밀번호)
# output :  게시글 삭제 성공 유무
@app.delete("/api/v1/board/{board_no}", name="게시글 삭제")
async def deleteBoard(
        password: str,
        board_no: int
):
    res_check = await checkBoard(board_no, password)

    if res_check['result'] is None:
        return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})

    if res_check['result']:
        result = await db.deleteBoard(password, board_no)

        if result is None:
            return JSONResponse(status_code=400, content={"message": "게시물 삭제에 실패했습니다."})
        return result
    else:
        return JSONResponse(status_code=400, content={"message": "비밀번호가 일치하지 않습니다."})


#  S04P22D101-62	백엔드 RESTful API 프로토콜 / 게시글 추천(좋아요 기능)
# input : board_no(보드번호)
# output : 좋아요 성공 유무 (중복 방지)
@app.post("/api/v1/board/like/{board_no}", name="게시글 추천(좋아요 기능)")
async def countUpThumbsUpOnBoard(
        board_no: int, request: Request
):
    ip = request.client.host
    res_check = await checkUserIpOnGoodList(board_no, ip)

    if res_check['result'] is None:
        return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})

    # 존재했으면 이미 누른 상태이므로 -1
    if res_check['result']:
        count_result = await db.countDownThumbsUpOnBoard(board_no)
        if count_result is None:
            return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})

        delete_result = await db.deleteUserIpOnGoodList(board_no, ip)
        if delete_result is None:
            await db.countUpThumbsUpOnBoard(board_no)
            return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})
        return "좋아요 취소"

    # 존재하지 않았음 좋아요+1
    else:
        count_result = await db.countUpThumbsUpOnBoard(board_no)
        if count_result is None:
            return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})
        insert_result = await db.insertUserIpOnGoodList(board_no, ip)

        if insert_result is None:
            await db.countDownThumbsUpOnBoard(board_no)
            return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})
        return "좋아요!"


# S04P22D101-105    추천 중복 방지
# input : board_no(보드번호), ip(유저ip)
# output : 좋아요 성공 유무 (중복 방지)
async def checkUserIpOnGoodList(
        board_no: int,
        ip: str,
):
    result = await db.checkUserIpOnGoodList(board_no, ip)
    return {"result": result}


### 여기까지 게시글 기능 종료 ###


### 여기부터 댓글 기능 시작 ###

#  S04P22D101-65     백엔드 RESTful API 프로토콜 / 댓글 조회 (해당 게시글에 대해)
@app.get("/api/v1/comment/{board_no}", name="댓글 조회")
async def findCommentByBoardNo(
        board_no: int
):
    result = await db.findCommentByBoardNo(board_no)

    if result is None:
        return JSONResponse(status_code=400, content={"message": "댓글 조회에 실패했습니다."})
    return result


#  S04P22D101-59	백엔드 RESTful API 프로토콜 / 댓글 작성
# input : board_no(보드번호), content(댓글 내용), nickname(닉네임), password(비밀번호)
# output : 댓글 작성 성공 유무
@app.post("/api/v1/comment/write/{board_no}", name="댓글 작성")
async def writeComment(
        board_no: int, content: str, nickname: str, password: str, request: Request
):
    ip = request.client.host
    comment_info = {
        "board_no": board_no,
        "content": content,
        "nickname": nickname,
        "password": password,
        "ip": ip,
    }

    result = await db.writeComment(comment_info)

    if result is None:
        return JSONResponse(status_code=400, content={"message": "댓글 작성에 실패했습니다."})
    return result


#  S04P22D101-61	백엔드 RESTful API 프로토콜 / 댓글 삭제
# input : comment_no(댓글번호), password(비밀번호)
# output : 댓글 삭제 성공 유무
@app.delete("/api/v1/comment/{comment_no}", name="댓글 삭제")
async def deleteComment(
        comment_no: int, password: str
):
    res_check = await checkComment(comment_no, password)

    if res_check['result'] is None:
        return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})

    if res_check['result']:
        result = await db.deleteComment(comment_no)

        if result is None:
            return JSONResponse(status_code=400, content={"message": "댓글 삭제에 실패했습니다."})
        return result
    else:
        return JSONResponse(status_code=400, content={"message": "비밀번호가 일치하지 않습니다."})


#  S04P22D101-66     백엔드 RESTful API 프로토콜 / 댓글 수정
# output : 댓글 수정 성공 유무
@app.put("/api/v1/comment/{comment_no}", name="댓글 수정")
async def editComment(
        comment_no: int, content: str, nickname: str, password: str, request: Request
):
    ip = request.client.host
    comment_info = {
        "comment_no": comment_no,
        "content": content,
        "nickname": nickname,
        "password": password,
        "ip": ip
    }

    res_check = await checkComment(comment_no, password)

    if res_check['result'] is None:
        return JSONResponse(status_code=400, content={"message": "작업중 에러가 발생했습니다."})

    if res_check['result']:
        result = await db.editComment(comment_info)

        if result is None:
            return JSONResponse(status_code=400, content={"message": "댓글 수정에 실패했습니다."})
        return result
    else:
        return JSONResponse(status_code=400, content={"message": "비밀번호가 일치하지 않습니다."})


#  S04P22D101-85     백엔드 RESTful API 프로토콜 / 게시글 비밀번호 체크
# input : comment_no(댓글번호), password(비밀번호)
# output : 비밀번호 매칭 유무
@app.post("/api/v1/board/check/{board_no}", name="게시글 비밀번호 체크")
async def checkBoard(
        board_no: int, password: str
):
    result = await db.checkPasswordOnBoard(password, board_no)
    return {"result": result}


#  S04P22D101-86     백엔드 RESTful API 프로토콜 / 댓글 비밀번호 체크
# input : comment_no(댓글번호), password(비밀번호)
# output : 비밀번호 매칭 유무
@app.post("/api/v1/comment/check/{comment_no}", name="댓글 비밀번호 체크")
async def checkComment(
        comment_no: int, password: str
):
    result = await db.checkPasswordOnComment(password, comment_no)
    return {"result": result}


### 여기까지 댓글 기능 종료 ###


# 데모 코드
@app.get("/")
async def read_root():
    return {"Hello": "World"}
# @app.post("/files/")
# async def create_file(
#     file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
# ):
#     return {
#         "file_size": len(file),
#         "token": token,
#         "fileb_content_type": fileb.content_type,
#     }


#
# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}
#
# @app.post("/files_old/")
# async def create_file(
#     file: UploadFile = File(...)
# ):
#     return {
#         "file_name": file.filename,
#         "file_size": len(file.file),
#         "file_content_type": file.content_type,
#     }
#
# @app.post("/files/")
# async def create_files(files: List[bytes] = File(...)):
#     return {"file_sizes": [len(file) for file in files]}
#
# @app.post("/uploadfiles")
# async def create_upload_files(files: List[UploadFile] = File(...)):
#     UPLOAD_DIRECTORY = "./"
#     for file in files:
#         contents = await file.read()
#         with open(os.path.join(UPLOAD_DIRECTORY, file.filename), "wb") as fp:
#             fp.write(contents)
#         print(file.filename)
#     return {"filenames": [file.filename for file in files]}