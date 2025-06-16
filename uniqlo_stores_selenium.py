from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

# --- 設定 Chrome 選項 ---
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized") # 最大化視窗
# 如果您不需要看到瀏覽器視窗，可以啟用無頭模式，程式會更快運行
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# --- 初始化 WebDriver ---
driver = webdriver.Chrome(options=options)

# 定義 HTML 檔案名稱
html_filename = "uniqlo_stores.html"

try:
    # --- 打開 Uniqlo 門市網頁 ---
    print("正在開啟網頁...")
    driver.get("https://www.uniqlo.com/tw/zh_TW/stores.html")

    # --- 等待頁面內容加載 ---
    print("等待門市資訊加載完成...")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "store_Info"))
    )
    print("門市資訊加載完成。")

    # --- 找到所有門市資訊的區塊 ---
    store_info_elements = driver.find_elements(By.CLASS_NAME, "store_Info")

    if not store_info_elements:
        print("警告：未找到任何門市資訊區塊。請再次檢查網頁的實際HTML結構或加載方式。")
    else:
        print(f"找到 {len(store_info_elements)} 個門市資訊區塊。")
        extracted_data = []

        # --- 迭代每個門市資訊區塊並提取資料 ---
        for i, store_element in enumerate(store_info_elements):
            store_data = {}
            # 提取店名
            try:
                store_name_element = store_element.find_element(By.CSS_SELECTOR, ".storeName p")
                store_data['店鋪名稱'] = store_name_element.text.strip()
            except Exception:
                store_data['店鋪名稱'] = "N/A"

            # 提取電話
            try:
                store_phone_element = store_element.find_element(By.CSS_SELECTOR, ".storePhone p")
                store_data['電話'] = store_phone_element.text.strip()
            except Exception:
                store_data['電話'] = "N/A"

            # 提取地址
            try:
                store_address_element = store_element.find_element(By.CSS_SELECTOR, ".storeAddress p")
                store_data['地址'] = store_address_element.text.strip()
            except Exception:
                store_data['地址'] = "N/A"

            # 提取網購店取
            try:
                online_pickup_element = store_element.find_element(By.CSS_SELECTOR, ".onlineGet p")
                store_data['網購取貨位置'] = online_pickup_element.text.strip()
            except Exception:
                store_data['網購取貨位置'] = "N/A"

            # --- 判斷店鋪類型 (收集所有符合的類型) ---
            found_types = []

            # 檢查超大型店
            try:
                store_element.find_element(By.CSS_SELECTOR, ".storeName span.superbigStore")
                found_types.append("超大型店")
            except:
                pass

            # 檢查大型店
            try:
                store_element.find_element(By.CSS_SELECTOR, ".storeName span.bigStore")
                found_types.append("大型店")
            except:
                pass

            # 檢查直營店
            try:
                store_element.find_element(By.CSS_SELECTOR, ".storeName span.directStore")
                found_types.append("直營店")
            except:
                pass

            # 如果沒有找到任何特定的類型，則設定為「一般店」
            if not found_types:
                store_data['店鋪類型'] = "一般店"
            else:
                # 將所有找到的類型用逗號連接起來
                store_data['店鋪類型'] = ", ".join(found_types)

            extracted_data.append(store_data)

        # --- 使用 pandas 創建 DataFrame ---
        columns_order = ['店鋪名稱', '店鋪類型', '地址', '電話', '網購取貨位置']
        df = pd.DataFrame(extracted_data, columns=columns_order)

        # --- 打印提取到的資料 (可選，但有助於驗證) ---
        print("\n--- 提取到的門市資料 (表格形式) ---")
        print(df.to_string(index=False))

        # --- 將 DataFrame 轉換為 HTML 表格 ---
        # index=False 避免在 HTML 表格中顯示 Pandas 的索引
        html_table = df.to_html(index=False, escape=False) # escape=False 避免對HTML實體編碼

        # --- 構建完整的 HTML 頁面內容 ---
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UNIQLO 台灣門市資料</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>UNIQLO 台灣門市資料</h1>
    {html_table}
</body>
</html>
        """

        # --- 將 HTML 內容寫入檔案 ---
        print(f"\n正在將資料儲存到 {html_filename} ...")
        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"資料已成功儲存到：{os.path.abspath(html_filename)}")
        print(f"您可以打開 {html_filename} 檔案來查看網頁。")

finally:
    # --- 關閉瀏覽器 ---
    print("\n關閉瀏覽器。")
    driver.quit()