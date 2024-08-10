#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymysql

# Selenium 설정
driver = webdriver.Chrome()
url = "https://www.google.com/search?q=메이플&hl=ko&tbm=nws"
driver.get(url)

# 페이지 로딩을 위해 잠시 대기
time.sleep(3)

# MySQL 데이터베이스 연결
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    db='maple',
    charset='utf8'
)
cursor = conn.cursor()

# 데이터베이스에 데이터를 삽입하는 함수
def insert_into_db(index, title, time_info):
    try:
        sql = "INSERT INTO maplenews_list (`index`, title, time) VALUES (%s, %s, %s)"
        cursor.execute(sql, (index, title, time_info))
        conn.commit()
        print(f"Inserted: Index {index}, Title: {title}, Time: {time_info}")
    except Exception as e:
        print(f"데이터베이스에 삽입 오류: {e}")

# 인덱스 값과 제목, 시간 정보 추출 함수
def extract_indexes():
    elems = driver.find_elements(By.CLASS_NAME, "n0jPhd")
    time_elems = driver.find_elements(By.CSS_SELECTOR, "div.OSrXXb span")  # 시간 정보 추출
    last_idx = None

    for idx, (elem, time_elem) in enumerate(zip(elems, time_elems), 1):
        try:
            title = elem.text
            time_info = time_elem.text  # 시간 정보 추출
            print(f"Index {idx}: {title}, Time: {time_info}")
            last_idx = idx
            # 데이터베이스에 인덱스와 제목, 시간 정보 삽입
            insert_into_db(idx, title, time_info)
        except Exception as e:
            print(f"Error on index {idx}: {e}")
            last_idx = idx

    print(f"Last Index: {last_idx}")

# 페이지 번호 추출 함수
def get_page_number():
    # 모든 페이지 버튼을 찾기
    page_buttons = driver.find_elements(By.CSS_SELECTOR, "td a.fl")
    
    for button in page_buttons:
        aria_label = button.get_attribute("aria-label")
        if aria_label and "Page" in aria_label:
            # aria-label 값에서 페이지 번호 추출
            page_number = int(aria_label.split("Page ")[-1])
            return page_number
    return None

# 모든 페이지를 클릭하는 함수
def click_all_pages():
    while True:
        # 현재 페이지 번호 추출
        current_page_number = get_page_number()
        
        if current_page_number is None:
            print("페이지 번호를 확인할 수 없습니다.")
            break
        
        # 현재 페이지의 인덱스 값과 제목, 시간 정보 추출
        extract_indexes()
        
        # 다음 페이지 버튼 클릭
        try:
            next_button = driver.find_element(By.ID, "pnnext")
            next_button.click()
            time.sleep(3)  # 페이지 로딩 대기
        except Exception as e:
            print(f"다음 페이지 버튼 클릭 오류: {e}")
            break

# 모든 페이지를 클릭하는 함수 호출
click_all_pages()

# 데이터베이스 연결 종료
cursor.close()
conn.close()

# 잠시 대기 후 종료
time.sleep(5)
driver.quit()




# %%
