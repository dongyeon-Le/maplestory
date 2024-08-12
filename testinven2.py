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

def extract_data_until_target_date(target_date):
    while True:
        # 현재 페이지에서 데이터 추출
        elems = driver.find_elements(By.CLASS_NAME, "subject-link")
        elems_date = driver.find_elements(By.CLASS_NAME, "date")
        elems_count = driver.find_elements(By.CLASS_NAME, "view")
        
        date_found = False
        for idx, (elem, elem_date, elem_count) in enumerate(zip(elems, elems_date, elems_count), 1):
            try:
                title = elem.text
                date = elem_date.text
                count = elem_count.text
                print(f"Index {idx}: {title} date:{date} count:{count}")

                # 목표 날짜가 발견되면 루프를 종료
                if date == target_date:
                    print(f"목표 날짜 {target_date}가 발견되었습니다. 종료합니다.")
                    date_found = True
                    break

            except Exception as e:
                print(f"Error on index {idx}: {e}")

        if date_found:
            break
        
        # 페이지 1부터 10까지 이동 후 다음 페이지 버튼 클릭
        try:
            page_numbers = driver.find_elements(By.CSS_SELECTOR, "By.LINK_TEXT")
            for page in range(1, 11):  # 페이지 1부터 10까지
                try:
                    page_link = next()
                    page_link.click()
                    time.sleep(3)  # 페이지 로딩 대기

                    # 데이터 추출
                    elems = driver.find_elements(By.CLASS_NAME, "subject-link")
                    elems_date = driver.find_elements(By.CLASS_NAME, "date")
                    elems_count = driver.find_elements(By.CLASS_NAME, "view")

                    date_found = False
                    for idx, (elem, elem_date, elem_count) in enumerate(zip(elems, elems_date, elems_count), 1):
                        try:
                            title = elem.text
                            date = elem_date.text
                            count = elem_count.text
                            print(f"Index {idx}: {title} date:{date} count:{count}")

                            # 목표 날짜가 발견되면 루프를 종료
                            if date == target_date:
                                print(f"목표 날짜 {target_date}가 발견되었습니다. 종료합니다.")
                                date_found = True
                                break

                        except Exception as e:
                            print(f"Error on index {idx}: {e}")

                    if date_found:
                        break
                    
                except StopIteration:
                    print(f"페이지 번호 {page}를 찾을 수 없습니다.")
                    break

            if date_found:
                break

            # 다음 페이지 버튼 클릭
            next_button = driver.find_element(By.CSS_SELECTOR, "#paging li a.next-btn")
            if 'disabled' in next_button.get_attribute('class'):
                print("다음 페이지가 없습니다.")
                break
            next_button.click()
            time.sleep(3)  # 페이지 로딩 대기

        except Exception as e:
            print("페이지 이동 중 오류 발생:", e)
            break

# 08-01이 나올 때까지 데이터 추출 시작
extract_data_until_target_date("07-01")

# 마지막으로 드라이버 종료
driver.quit()

# %%
