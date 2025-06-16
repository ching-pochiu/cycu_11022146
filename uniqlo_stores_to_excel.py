from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.uniqlo.com/tw/zh_TW/stores.html")
time.sleep(8)  # 等待JS載入

stores = driver.find_elements(By.CSS_SELECTOR, ".store_Info")
data = []
for store in stores:
    name = store.find_element(By.CSS_SELECTOR, ".storeName p").text
    phone = store.find_element(By.CSS_SELECTOR, ".storePhone p").text
    address = store.find_element(By.CSS_SELECTOR, ".storeAddress p").text
    online_get = store.find_element(By.CSS_SELECTOR, ".onlineGet p").text
    # 你可以根據需求拆分店名/型態、地址等
    data.append([name, address, phone, online_get])

driver.quit()

# 儲存成 Excel
df = pd.DataFrame(data, columns=["店鋪名稱", "地址", "電話", "網購取貨位置"])
df.to_excel("uniqlo_stores.xlsx", index=False)
print("已儲存為 uniqlo_stores.xlsx")