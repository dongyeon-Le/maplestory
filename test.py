#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
url = "https://www.google.com/search?q=메이플&hl=ko&tbm=nws"
driver.get(url)

def extract_indexes():
    elems = driver.find_elements(By.CLASS_NAME, "n0jPhd.ynAwRc.MBeuO.nDgy9d")
    last_idx = None

    for idx, elem in enumerate(elems, 1):
        try:
            name = elem.text
            print(f"Index {idx}: {name}")
            last_idx = idx
        except Exception as e:
            print(f"Error on index {idx}: {e}")
            last_idx = idx

    print(f"Last Index: {last_idx}")

extract_indexes()


# %%
