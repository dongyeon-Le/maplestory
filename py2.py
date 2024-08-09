#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from urllib.request import urlretrieve
import os
import time

driver = webdriver.Chrome()
url = "https://www.google.com/imghp?hl=ko&ogbl"
driver.get(url)

elem = driver.find_element(By.NAME,"q")
search = "메이플"
elem.send_keys(search)
elem.send_keys(Keys.ENTER)

elems = driver.find_elements(By.CLASS_NAME,"ob5Hkd")

for idx,elem in enumerate(elems,1):
    try:
        elem.click()
        driver.implicitly_wait(3)
        img = driver.find_element(By.CSS_SELECTOR,"sFlh5c pT0Scc iPVvYb").get_attribute('src')
        print(elem)
    except:
        print(elem)
# %%
