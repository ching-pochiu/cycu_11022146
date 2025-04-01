import html
import pandas as pd
from bs4 import BeautifulSoup

# 讀取本地 HTML 檔案
with open("bus1.html", "r", encoding="utf-8") as file:
    content = file.read()

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(content, "html.parser")

# 初始化去程與返程的資料
outbound_data = []  # 去程資料
inbound_data = []   # 返程資料

# 解析去程資料 (class="ttego1" 和 class="ttego2")
for tr in soup.find_all("tr", class_=["ttego1", "ttego2"]):
    td = tr.find("td")
    if td:
        stop_name = html.unescape(td.text.strip())  # 解碼站點名稱
        stop_link = td.find("a")["href"] if td.find("a") else None
        outbound_data.append({"站點名稱": stop_name, "連結": stop_link})

# 解析返程資料 (class="tteback1" 和 class="tteback2")
for tr in soup.find_all("tr", class_=["tteback1", "tteback2"]):
    td = tr.find("td")
    if td:
        stop_name = html.unescape(td.text.strip())  # 解碼站點名稱
        stop_link = td.find("a")["href"] if td.find("a") else None
        inbound_data.append({"站點名稱": stop_name, "連結": stop_link})

# 將資料轉換為 DataFrame
outbound_df = pd.DataFrame(outbound_data)
inbound_df = pd.DataFrame(inbound_data)

# 輸出結果
if not outbound_df.empty:
    print("去程資料：")
    print(outbound_df)
    outbound_df.to_csv("outbound.csv", index=False, encoding="utf-8-sig")
else:
    print("未找到去程資料。")

if not inbound_df.empty:
    print("\n返程資料：")
    print(inbound_df)
    inbound_df.to_csv("inbound.csv", index=False, encoding="utf-8-sig")
else:
    print("未找到返程資料。")