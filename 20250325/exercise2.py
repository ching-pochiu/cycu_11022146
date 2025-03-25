from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# 設定 ChromeDriver 路徑
chrome_driver_path = "path/to/chromedriver"  # 替換為您的 chromedriver 路徑
service = Service(chrome_driver_path)

# 啟動瀏覽器
driver = webdriver.Chrome(service=service)

# 開啟目標網址
url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"
driver.get(url)

# 等待網頁加載
time.sleep(5)

# 抓取「去程」資料
try:
    go_section = driver.find_element(By.ID, "go")  # 假設「去程」的區塊有 id="go"
    print("去程資料:")
    print(go_section.text)
except Exception as e:
    print(f"無法找到去程資料: {e}")

# 抓取「返程」資料
try:
    back_section = driver.find_element(By.ID, "back")  # 假設「返程」的區塊有 id="back"
    print("返程資料:")
    print(back_section.text)
except Exception as e:
    print(f"無法找到返程資料: {e}")

# 關閉瀏覽器
driver.quit()