#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pymysql


driver = webdriver.Chrome()
url = "https://www.google.com/imghp?hl=ko&ogbl"
driver.get(url)

elem = driver.find_element(By.NAME,"q")
search = "메이플"
elem.send_keys(search)
elem.send_keys(Keys.ENTER)
driver.implicitly_wait(3)

##elements = driver.find_elements(By.ID, "hdtb-tls")
##elements[0].click()
##driver.implicitly_wait(3)

##elements = driver.find_elements(By.CLASS_NAME, "KTBKoe")
##elements[4].click()
##driver.implicitly_wait(3)

##last_year_filter = driver.find_element(By.XPATH, "//div[@jsname='ibnC6b' and @role='none']//a[contains(text(), '모든 날짜')]")
##last_year_filter.click()
##driver.implicitly_wait(3)

# 스크롤하여 더 많은 이미지 로드
scroll_pause_time = 2  # 스크롤 후 대기 시간
scrolling = True
last_height = driver.execute_script("return document.body.scrollHeight")

elems = []
while scrolling:
    elems = driver.find_elements(By.CLASS_NAME, "ob5Hkd")
    
    # 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)
    
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        scrolling = False
    last_height = new_height

elems = driver.find_elements(By.CLASS_NAME,"toI8Rb.OSrXXb")
last_idx = None

for idx, elem in enumerate(elems, 1):
    try:
        name = elem.text
        print(f"Index {idx}: {name}")
        last_idx = idx
    except Exception as e:
        print(f"Error on index {idx}: {e}")
        last_idx = idx

print(last_idx)

conn = pymysql.connect(
host='localhost',
user='root',
password='1234',
db='maple',
charset='utf8'
)

cur.execute("INSERT INTO stat_average (average_stat, leng) VALUES (%d, %d);" %(sum / leng, leng))



# %%

