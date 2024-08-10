#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pymysql

# Selenium 설정
driver = webdriver.Chrome()
url = "https://www.google.com/imghp?hl=ko&ogbl"
driver.get(url)

elem = driver.find_element(By.NAME,'q')
search = "메이플"
elem.send_keys(search)
elem.send_keys(Keys.ENTER)
driver.implicitly_wait(3)

##elements = driver.find_elements(By.ID, "hdtb-tls")
##elements[0].click()
##driver.implicitly_wait(3)

elements = driver.find_elements(By.CLASS_NAME, "YmvwI")
elements[2].click()
driver.implicitly_wait(3)

##last_year_filter = driver.find_element(By.XPATH, "//div[@jsname='ibnC6b' and @role='none']//a[contains(text(), '모든 날짜')]")
##last_year_filter.click()
##driver.implicitly_wait(3)


# 데이터베이스 연결
##conn = pymysql.connect(
##    host='localhost',
##    user='root',
##    password='1234',
##    db='maple',
##    charset='utf8'
## )
##cur = conn.cursor()

# 데이터 삽입
for idx, elem in enumerate(elems, 1):
    try:
        name = elem.text
        print(f"Index {idx}: {name}")

        # 데이터베이스에 삽입
        sql = "INSERT INTO maple_list (`index`, title) VALUES (%s, %s)"
        cur.execute(sql, (idx, name))
        conn.commit()
        last_idx = idx
    except Exception as e:
        print(f"Error on index {idx}: {e}")
        last_idx = idx

print(last_idx)

# 데이터베이스 연결 종료
cur.close()
conn.close()

# %%
