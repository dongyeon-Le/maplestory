# %%
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil import parser
import re

# MySQL 데이터베이스에 연결
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'maple'
}

def parse_relative_time(relative_time):
    now = datetime.now()
    if '시간 전' in relative_time:
        hours = int(re.findall(r'\d+', relative_time)[0])
        return now - timedelta(hours=hours)
    elif '일 전' in relative_time:
        days = int(re.findall(r'\d+', relative_time)[0])
        return now - timedelta(days=days)
    elif '주 전' in relative_time:
        weeks = int(re.findall(r'\d+', relative_time)[0])
        return now - timedelta(weeks=weeks)
    elif '개월 전' in relative_time:
        months = int(re.findall(r'\d+', relative_time)[0])
        return now - timedelta(days=30*months)
    elif '년 전' in relative_time:
        years = int(re.findall(r'\d+', relative_time)[0])
        return now - timedelta(days=365*years)
    else:
        # '방금 전' 또는 기타 시간 표현 처리
        return now

try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "SELECT title, time FROM maplenews_list ORDER BY time DESC"
    cursor.execute(query)
    results = cursor.fetchall()

    # 데이터프레임으로 변환
    df = pd.DataFrame(results, columns=['Title', 'Time'])

    # 상대적 시간 처리
    df['Time'] = df['Time'].apply(parse_relative_time)

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
    if connection.is_connected():
        cursor.close()
        connection.close()

# %%
