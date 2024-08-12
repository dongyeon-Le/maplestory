#%%
import mysql.connector
import matplotlib.pyplot as plt

# MySQL 데이터베이스 연결
connection = mysql.connector.connect(
    host="localhost",       # 호스트 주소 (예: "localhost")
    user="root",   # MySQL 사용자명
    password="1234", # MySQL 비밀번호
    database="maple"  # 데이터베이스 이름
)

# 커서 생성
cursor = connection.cursor()

# SQL 쿼리 실행
query = """
SELECT
    CASE 
        WHEN time LIKE '%2024. 1%' THEN '1월'
        WHEN time LIKE '%2024. 2%' THEN '2월'
        WHEN time LIKE '%2024. 3%' THEN '3월'
        WHEN time LIKE '%2024. 4%' THEN '4월'
        WHEN time LIKE '%2024. 5%' THEN '5월'
        WHEN time LIKE '%2024. 6%' THEN '6월'
        WHEN time LIKE '%시간 전%' OR time LIKE '%개월 전%' OR time LIKE '%주 전%' OR time LIKE '%일 전%' THEN '7월'
        ELSE '기타'
    END AS 월,
    COUNT(*) AS 카운트
FROM maplenews_list
GROUP BY 월
ORDER BY 
    CASE 
        WHEN 월 = '1월' THEN 1
        WHEN 월 = '2월' THEN 2
        WHEN 월 = '3월' THEN 3
        WHEN 월 = '4월' THEN 4
        WHEN 월 = '5월' THEN 5
        WHEN 월 = '6월' THEN 6
        WHEN 월 = '7월' THEN 7
        ELSE 8
    END;
"""
cursor.execute(query)

# 쿼리 결과 가져오기
results = cursor.fetchall()

plt.hist(results,'월')

# MySQL 연결 종료
cursor.close()
connection.close()

# %%
