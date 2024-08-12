#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Selenium 설정
driver = webdriver.Chrome()
url = "https://www.inven.co.kr/board/maple/5974?my=chuchu"
driver.get(url)

# 페이지 로딩을 위해 잠시 대기
time.sleep(3)


# 현재 페이지에서 게시글 정보 추출
def extract_data():
    elems = driver.find_elements(By.CLASS_NAME, "subject-link")
    elems_date = driver.find_elements(By.CLASS_NAME, "date")
    elems_count = driver.find_elements(By.CLASS_NAME, "view")
    
    for idx, (elem, elem_date, elem_count) in enumerate(zip(elems, elems_date, elems_count), 1):
        try:
            title = elem.text
            date = elem_date.text
            count = elem_count.text
            print(f"Index {idx}: {title} date:{date} count:{count}")
        except Exception as e:
            print(f"Error on index {idx}: {e}")




# 모든 페이지를 클릭하는 함수
def click_all_pages():
    while True:
    extract_indexes()
      try:
       for page_number in range(1, 11):
        page_link = driver.find_element(By.LINK_TEXT, str(page_number))
        page_link.click()
        time.sleep(3)  # 페이지 로딩 대기
      except Exception as e:
        print(f"페이지 {page_number}로 이동 오류: {e}")
        
        # 다음 페이지 버튼 클릭
        try:
            next_button = driver.find_element(By.ID, "pnnext")
            next_button.click()
            time.sleep(3)  # 페이지 로딩 대기
        except Exception as e:
            print(f"다음 페이지 버튼 클릭 오류: {e}")
            break

# 마지막으로 드라이버 종료
driver.quit()



# %%
