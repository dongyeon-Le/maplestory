# %%
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
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
    elif '2024. 1' in relative_time:
        years = int(re.findall(r'\d+', relative_time)[0])
        return now - timedelta(days=365*years)
    else:
        return now

try:
    # 데이터베이스 연결
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    
    # 쿼리 작성
    query = "SELECT title, time FROM maplenews_list ORDER BY time DESC"
    
    # 쿼리 실행
    cursor.execute(query)
    
    # 결과 가져오기
    results = cursor.fetchall()
    
    # 데이터프레임으로 변환
    df = pd.DataFrame(results, columns=['Title', 'Time'])

    # 상대적 시간 처리
    df['Time'] = df['Time'].apply(parse_relative_time)
    
    # 시간대별로 그룹화
    df['Hour'] = df['Time'].dt.floor('H')
    hour_counts = df.groupby('Hour').size()
    
    # 그래프 그리기
    plt.figure(figsize=(12, 6))
    hour_counts.plot(kind='bar', color='skyblue')
    plt.xlabel('Hour')
    plt.ylabel('Count')
    plt.title('Number of Entries by Hour')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

except mysql.connector.Error as err:
    print(f"Database Error: {err}")
except pd.errors.EmptyDataError:
    print("No data returned from query.")
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 연결 닫기
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()

# %%
