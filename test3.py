#%%
import mysql.connector

# MySQL 데이터베이스에 연결
db_config = {
    'host': 'localhost',       # 데이터베이스 서버 호스트 (예: 'localhost' 또는 IP 주소)
    'user': 'root',    # MySQL 사용자 이름
    'password': '1234',# MySQL 사용자 비밀번호
    'database': 'maple' # 연결할 데이터베이스 이름
}

try:
    # 데이터베이스 연결
    connection = mysql.connector.connect(**db_config)

    # 커서 생성
    cursor = connection.cursor()

    # 쿼리 작성
    query = "SELECT title,time FROM maplenews_list order by time desc"

    # 쿼리 실행
    cursor.execute(query)

    # 결과 가져오기
    results = cursor.fetchall()

    # 결과 출력
    for row in results:
        title, time = row
        print(f"Title: {title}, Time:{time}")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # 연결 닫기
    if connection.is_connected():
        cursor.close()
        connection.close()

# %%
