import mysql.connector

# DB 연결

mydb = mysql.connector.connect(
    host="j4d101.p.ssafy.io",
    user="ssafy",
    password="head101@",
    database="jjal"
)
cursor = mydb.cursor()
print(mydb)


### 여기부터 게시글 기능 시작 ###


#  S04P22D101-63	백엔드 RESTful API 프로토콜 / 최근 게시글들 조회(추천순 반영)
async def findAllBoardOnDay():
    cursor.execute("SELECT * FROM board")
    res = cursor.fetchall()
    result = []
    for item in res:
        result.append({'board_no': item[0],
                       'title': item[1],
                       'content': item[2],
                       'content_type': item[3],
                       'nickname': item[4],
                       # 'password' : item[5],
                       'ip': item[6],
                       'good': item[7],
                       'regdate': item[8]
                       })
    return result


#  S04P22D101-64     백엔드 RESTful API 프로토콜 / 게시글 상세 조회
async def findBoardDetailByBoardNo(
        board_no: int
):
    pass
    sql = "SELECT * FROM board WHERE board_no = %s"
    cursor.execute(sql, (board_no,))
    res = cursor.fetchone()
    if res is None:
        return None
    return {'board_no': res[0],
            'title': res[1],
            'content': res[2],
            'content_type': res[3],
            'nickname': res[4],
            # 'password' : res[5],
            'ip': res[6],
            'good': res[7],
            'regdate': res[8]
            }

#  S04P22D101-57	백엔드 RESTful API 프로토콜 / 게시글 작성(공유)
async def writeBoard(
        board_info: dict
):
    pass
    sql = """
            INSERT INTO board (title, content, content_type, nickname, password, ip)
            VALUES (%s, %s, %s, %s, %s, %s)
          """
    val = (board_info.title, board_info.content, board_info.content_type,
           board_info.nickname, board_info.password, board_info.ip)
    cursor.execute(sql, val)
    mydb.commit()
    print(cursor.rowcount, "board inserted.")


#  S04P22D101-67     백엔드 RESTful API 프로토콜 / 게시글 수정
async def editBoard(
        board_info: dict
):
    pass
    # 비밀번호 ??
    sql = """
            UPDATE board 
            SET title = %s, content = %s, content_type = %s, 
                nickname = %s, password = %s, ip = %s
            WHERE board_no = %s
          """
    val = (board_info.title, board_info.content, board_info.content_type,
           board_info.nickname, board_info.password, board_info.ip)

    cursor.execute(sql, val)
    mydb.commit()
    print(cursor.rowcount, "board updated.")


#  S04P22D101-60	백엔드 RESTful API 프로토콜 / 게시글 삭제
async def deleteBoard(
        password: str
):
    pass
    # 비밀번호 ??
    sql = "DELETE FROM board WHERE board_no = %s"
    val = password
    cursor.execute(sql, val)
    mydb.commit()
    print(cursor.rowcount, "board deleted.")


#  S04P22D101-62	백엔드 RESTful API 프로토콜 / 게시글 추천(좋아요 기능)
async def countUpThumbsUpOnBoard(
        board_no: int, ip: str
):
    pass
    sql = """
                UPDATE board 
                SET good = good+1
                WHERE board_no = %s
              """
    val = board_no
    cursor.execute(sql, val)
    mydb.commit()
    print(cursor.rowcount, "board updated.")


### 여기까지 게시글 기능 종료 ###


### 여기부터 댓글 기능 시작 ###


#  S04P22D101-65     백엔드 RESTful API 프로토콜 / 댓글 조회 (해당 게시글에 대해)
async def findCommentByBoardNo(
        board_no: int
):
    pass
    sql = """
            SELECT * 
              FROM comment 
             WHERE board_no = %s
          """
    val = board_no
    cursor.execute(sql, val)
    res = cursor.fetchall()
    return res


#  S04P22D101-59	백엔드 RESTful API 프로토콜 / 댓글 작성
async def writeComment(
        comment_info: dict
):
    pass
    sql = """
            INSERT INTO comment (board_no, content, nickname, password, ip)
            VALUES (%s, %s, %s, %s, %s, %s)
          """
    val = (comment_info.board_no, comment_info.content,
           comment_info.nickname, comment_info.password, comment_info.ip)
    cursor.execute(sql, val)
    mydb.commit()
    print(cursor.rowcount, "board inserted.")


#  S04P22D101-61	백엔드 RESTful API 프로토콜 / 댓글 삭제
async def deleteComment(
        comment_no: int, password: str
):
    pass
    # 비밀번호 ??
    sql = """DELETE FROM comment 
    WHERE comment_no = %s AND password = %s"""
    val = (comment_no, password)
    cursor.execute(sql, val)
    mydb.commit()
    print(cursor.rowcount, "board deleted.")


#  S04P22D101-66     백엔드 RESTful API 프로토콜 / 댓글 수정
async def editComment(
        comment_info: dict
):
    pass
    sql = """
            UPDATE comment 
            SET content = %s
            WHERE comment_no = %s
          """
    val = (comment_info.content, comment_info.comment_no)
    cursor.execute(sql, val)
    mydb.commit()
    print(cursor.rowcount, "board updated.")
### 여기까지 댓글 기능 종료 ###
