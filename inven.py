#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymysql

# Selenium 설정
driver = webdriver.Chrome()
url = "https://www.inven.co.kr/board/maple/5974?my=chuchu"
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
        sql = "INSERT INTO mapleinven_list (title, date, count) VALUES (%s, %s, %s)"
        cursor.execute(sql, (index, title, time_info))
        conn.commit()
    except Exception as e:
        print(f"데이터베이스에 삽입 오류: {e}")

# 전역 변수로 날짜 발견 여부 추적
date_found = False

# 현재 페이지에서 게시글 정보 추출
def extract_data():
    global date_found
    elems = driver.find_elements(By.CLASS_NAME, "subject-link")
    elems_date = driver.find_elements(By.CLASS_NAME, "date")
    elems_count = driver.find_elements(By.CLASS_NAME, "view")
    
    for idx, (elem, elem_date, elem_count) in enumerate(zip(elems, elems_date, elems_count), 1):
        try:
            title = elem.text
            date = elem_date.text
            count_text = elem_count.text
            
            # count_text가 숫자만 포함되어 있는지 확인 후 정수로 변환
            count = int(count_text.replace(',', '').strip())

            print(f"Index {idx}: {title} date:{date} count:{count}")
            insert_into_db(title, date, count)

            # 목표 날짜가 발견되면 루프 종료 신호
            if date == "08-03":
                print(f"목표 날짜 {date}가 발견되었습니다. 데이터 추출 중지합니다.")
                date_found = True
                return  # 데이터 추출을 종료하고 루프를 중단합니다

        except Exception as e:
            print(f"Error on index {idx}: {e}")

# 모든 페이지를 클릭하는 함수
def click_all_pages():
    global date_found
    page_group = 1
    
    while not date_found:
        # 페이지 그룹 클릭
        try:
            # 페이지 링크들 가져오기
            page_links = driver.find_elements(By.CSS_SELECTOR, "#paging li a")
            page_numbers = [int(link.text) for link in page_links if link.text.isdigit()]
            
            # 현재 페이지 그룹에 해당하는 페이지들 클릭
            start_page = (page_group - 1) * 10 + 1
            end_page = page_group * 10
            
            for page_number in range(start_page, end_page + 1):
                if page_number in page_numbers:
                    try:
                        page_link = driver.find_element(By.LINK_TEXT, str(page_number))
                        page_link.click()
                        time.sleep(3)  # 페이지 로딩 대기
                        extract_data()
                        if date_found:
                            return  # 날짜 발견 시 페이지 탐색 중단
                    except Exception as e:
                        print(f"페이지 {page_number} 클릭 오류: {e}")

            # 페이지 그룹 증가
            page_group += 1

            # 다음 페이지 버튼 클릭
            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "#paging li a.next-btn")
                if 'disabled' in next_button.get_attribute('class'):
                    print("다음 페이지가 없습니다. 모든 페이지를 처리했습니다.")
                    break
                next_button.click()
                time.sleep(3)  # 페이지 로딩 대기
            except Exception as e:
                print(f"다음 페이지 버튼 클릭 오류: {e}")
                break

        except Exception as e:
            print(f"페이지 이동 오류: {e}")
            break

# 데이터 추출 시작
click_all_pages()

# 데이터베이스 연결 종료
cursor.close()
conn.close()

# 잠시 대기 후 종료
time.sleep(5)

# 마지막으로 드라이버 종료
driver.quit()

# %%
