# %%
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

# MySQL 데이터베이스에 연결
db_config = {
    'host': 'localhost',       # 데이터베이스 서버 호스트
    'user': 'root',            # MySQL 사용자 이름
    'password': '1234',        # MySQL 사용자 비밀번호
    'database': 'maple'        # 연결할 데이터베이스 이름
}

try:
    # 데이터베이스 연결
    connection = mysql.connector.connect(**db_config)

    # 커서 생성
    cursor = connection.cursor()

    # 쿼리 작성
    query = "SELECT title, time FROM maplenews_list ORDER BY time DESC"

    # 쿼리 실행
    cursor.execute(query)

    # 결과 가져오기
    results = cursor.fetchall()

    # 결과를 데이터프레임으로 변환
    df = pd.DataFrame(results, columns=['Title', 'Time'])

    # 'Time' 열을 datetime 형식으로 변환
    df['Time'] = pd.to_datetime(df['Time'])

    # 그래프 그리기
    plt.figure(figsize=(12, 6))
    plt.bar(df['Time'], df['Title'], width=0.5, color='skyblue')
    plt.xlabel('Time')
    plt.ylabel('Title')
    plt.title('Titles by Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # 연결 닫기
    if connection.is_connected():
        cursor.close()
        connection.close()

# %%
