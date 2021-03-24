from mysql.connector import connect, Error
import datetime as dt
from config import config

# DB 연결

# GPU서버는 SQL서버와 통신이 불가하므로 예외처리
if not config.IS_GPU_SERVER:
    database = connect(
        host="j4d101.p.ssafy.io",
        user="ssafy",
        password="head101@",  # NOSONAR
        database="jjal"
    )
    cursor = database.cursor()
else:
    database = None
    cursor = None

# print(mydb)


# 여기부터 공용 기능 시작 ###

async def check_password_on_board(
        password: str,
        board_no: int
):
    # 해당 게시물 비밀번호 얻어오기
    sql = "SELECT password FROM board WHERE board_no = %s"

    try:
        cursor.execute(sql, (board_no,))
        res = cursor.fetchone()
        for pwd in res:
            if pwd == password:
                return True
            else:
                return False

    except Error as e:
        print(e)
        return None


async def check_password_on_comment(
        password: str,
        comment_no: int
):
    # 해당 게시물 비밀번호 얻어오기
    sql = "SELECT password FROM comment WHERE comment_no = %s"
    try:
        cursor.execute(sql, (comment_no,))
        res = cursor.fetchone()
        for pwd in res:
            if pwd == password:
                return True
            else:
                return False

    except Error as e:
        print(e)
        return None


async def check_user_ip_on_good_list(
        board_no: int,
        ip: str
):
    # 좋아요를 눌렀는지 안눌렀는지 확인하기
    sql = """
            SELECT IP FROM goodlist 
            WHERE board_no = %s AND ip = %s
          """
    try:
        cursor.execute(sql, (board_no, ip))
        res = cursor.fetchone()
        if res is None:
            return False
        else:
            return True

    except Error as e:
        print(e)
        return None


async def insert_user_ip_on_good_list(
        board_no: int,
        ip: str,
):
    sql = """
            INSERT INTO goodlist (board_no, ip)
            VALUES (%s, %s)
          """
    val = (board_no, ip)
    try:
        cursor.execute(sql, val)
        database.commit()
        return True

    except Error as e:
        print(e)
        return None


async def delete_user_ip_on_good_list(
        board_no: int,
        ip: str,
):
    sql = """
            DELETE FROM goodlist 
            WHERE board_no = %s AND ip = %s;
          """
    val = (board_no, ip)
    try:
        cursor.execute(sql, val)
        database.commit()
        return True

    except Error as e:
        print(e)
        return None


# 여기까지 공용 기능 종료 ###


# 여기부터 게시글 기능 시작 ###


#  S04P22D101-63	백엔드 RESTful API 프로토콜 / 최근 게시글들 조회(추천순 반영)
async def find_all_board_on_day():
    try:
        cursor.execute("SELECT * FROM board")
        res = cursor.fetchall()
        result = []
        for item in res:
            spilited_ip = item[6].split('.')

            idx = 0
            spilited_ip[2] = 'x'
            spilited_ip[3] = 'x'

            ip = ''
            for s in spilited_ip:
                ip += s
                idx = idx + 1
                if idx != 4:
                    ip += '.'
            result.append({'board_no': item[0],
                           'title': item[1],
                           'content': item[2],
                           'content_type': item[3],
                           'nickname': item[4],
                           # 'password' : item[5],
                           'ip': ip,
                           'good': item[7],
                           'regdate': item[8]
                           })
        return result
    except Error as e:
        print(e)
        return None


#  S04P22D101-64     백엔드 RESTful API 프로토콜 / 게시글 상세 조회
async def find_board_detail_by_board_no(
        board_no: int
):
    sql = "SELECT * FROM board WHERE board_no = %s"

    try:
        cursor.execute(sql, (board_no,))
        res = cursor.fetchone()
        if res is None:
            return None

        spilited_ip = res[6].split('.')

        idx = 0
        spilited_ip[2] = 'x'
        spilited_ip[3] = 'x'

        ip = ''
        for s in spilited_ip:
            ip += s
            idx = idx + 1
            if idx != 4:
                ip += '.'

        return {'board_no': res[0],
                'title': res[1],
                'content': res[2],
                'content_type': res[3],
                'nickname': res[4],
                # 'password' : res[5],
                'ip': ip,
                'good': res[7],
                'regdate': res[8]
                }
    except Error as e:
        print(e)
        return None


#  S04P22D101-57	백엔드 RESTful API 프로토콜 / 게시글 작성(공유)
async def write_board(
        board_info: dict
):
    print(board_info)
    sql = """
            INSERT INTO board (title, content, content_type, nickname, password, ip, regdate)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
          """
    val = (board_info['title'], board_info['content'], board_info['content_type'],
           board_info['nickname'], board_info['password'], board_info['ip'], dt.datetime.now())
    try:
        cursor.execute(sql, val)
        database.commit()
        return "게시물 작성에 성공했습니다."

    except Error as e:
        print(e)
        return None


#  S04P22D101-67     백엔드 RESTful API 프로토콜 / 게시글 수정
async def edit_board(
        board_info: dict
):
    # 비밀번호 ??
    sql = """
            UPDATE board 
            SET title = %s, content = %s, content_type = %s, 
                nickname = %s, password = %s, ip = %s
            WHERE board_no = %s
          """
    val = (board_info['title'], board_info['content'], board_info['content_type'],
           board_info['nickname'], board_info['password'],
           board_info['ip'], board_info['board_no'])
    try:
        cursor.execute(sql, val)
        database.commit()
        return "게시물 수정에 성공했습니다."
    except Error as e:
        print(e)
        return None


#  S04P22D101-60	백엔드 RESTful API 프로토콜 / 게시글 삭제
async def delete_board(
        board_no: int
):
    # 비밀번호 ??
    sql = "DELETE FROM board WHERE board_no = %s"
    val = (board_no,)
    try:
        cursor.execute(sql, val)
        database.commit()
        return "게시물 삭제에 성공했습니다."
    except Error as e:
        print(e)
        return None


#  S04P22D101-62	백엔드 RESTful API 프로토콜 / 게시글 추천(좋아요 기능)
async def count_up_thumbs_up_on_board(
        board_no: int
):
    sql = """
                UPDATE board 
                SET good = good+1
                WHERE board_no = %s
          """
    val = (board_no,)
    try:
        cursor.execute(sql, val)
        database.commit()
        return "좋아요!"

    except Error as e:
        print(e)
        return None


#  S04P22D101-62	백엔드 RESTful API 프로토콜 / 게시글 추천(좋아요 기능)
async def count_down_thumbs_up_on_board(
        board_no: int
):
    sql = """
                UPDATE board 
                SET good = good-1
                WHERE board_no = %s
          """
    val = (board_no,)
    try:
        cursor.execute(sql, val)
        database.commit()
        return True

    except Error as e:
        print(e)
        return None


# 여기까지 게시글 기능 종료 ###


# 여기부터 댓글 기능 시작 ###


#  S04P22D101-65     백엔드 RESTful API 프로토콜 / 댓글 조회 (해당 게시글에 대해)
async def find_comment_by_board_no(
        board_no: int
):
    sql = """
            SELECT * 
              FROM comment 
             WHERE board_no = %s
          """
    val = (board_no,)
    try:
        cursor.execute(sql, val)
        res = cursor.fetchall()
        result = []
        for item in res:
            spilited_ip = item[5].split('.')

            idx = 0
            spilited_ip[2] = 'x'
            spilited_ip[3] = 'x'

            ip = ''
            for s in spilited_ip:
                ip += s
                idx = idx + 1
                if idx != 4:
                    ip += '.'

            result.append({'comment_no': item[0],
                           'board_no': item[1],
                           'content': item[2],
                           'nickname': item[3],
                           # 'password' : item[4],
                           'ip': ip,
                           'regdate': item[6]
                           })
        return result

    except Error as e:
        print(e)
        return None


#  S04P22D101-59	백엔드 RESTful API 프로토콜 / 댓글 작성
async def write_comment(
        comment_info: dict
):
    sql = """
            INSERT INTO comment (board_no, content, nickname, password, ip, regdate)
            VALUES (%s, %s, %s, %s, %s, %s)
          """
    val = (comment_info['board_no'], comment_info['content'],
           comment_info['nickname'], comment_info['password'],
           comment_info['ip'], dt.datetime.now())
    try:
        cursor.execute(sql, val)
        database.commit()
        return "댓글 작성에 성공했습니다."

    except Error as e:
        print(e)
        return None


#  S04P22D101-61	백엔드 RESTful API 프로토콜 / 댓글 삭제
async def delete_comment(
        comment_no: int
):
    # 비밀번호 ??
    sql = """
            DELETE FROM comment 
            WHERE comment_no = %s
          """
    val = (comment_no,)
    try:
        cursor.execute(sql, val)
        database.commit()
        return "댓글 삭제에 성공했습니다."

    except Error as e:
        print(e)
        return None


#  S04P22D101-66     백엔드 RESTful API 프로토콜 / 댓글 수정
async def edit_comment(
        comment_info: dict
):
    pass
    sql = """
            UPDATE comment 
            SET content = %s, nickname = %s, password = %s, ip = %s
            WHERE comment_no = %s
          """
    val = (comment_info['content'], comment_info['nickname'],
           comment_info['password'], comment_info['ip'],
           comment_info['comment_no'])
    try:
        cursor.execute(sql, val)
        database.commit()
        return "댓글 수정에 성공했습니다."

    except Error as e:
        print(e)
        return None

# 여기까지 댓글 기능 종료 ###
