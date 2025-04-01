import os
import pandas as pd
from bs4 import BeautifulSoup

def load_bus_data(directory):
    """讀取並解析目錄中的所有 HTML 檔案，返回去程與返程的資料"""
    outbound_data = []  # 去程資料
    inbound_data = []   # 返程資料

    # 遍歷目錄中的所有 HTML 檔案
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            soup = BeautifulSoup(content, "html.parser")

            # 解析去程資料 (class="ttego1" 和 class="ttego2")
            for tr in soup.find_all("tr", class_=["ttego1", "ttego2"]):
                tds = tr.find_all("td")
                if len(tds) >= 4:  # 確保有足夠的 <td> 元素
                    route = tds[0].text.strip()  # 路線名稱
                    stop_name = tds[1].text.strip()  # 站牌名稱
                    direction = tds[2].text.strip()  # 去返程
                    stop_time = tds[3].get("data-deptimen1", "未知")  # 預估到站時間
                    # 如果 stop_time 是數字，轉換為分鐘數
                    if stop_time.isdigit():
                        stop_time = f"{stop_time} 分鐘後到達"
                    else:
                        stop_time = "未知"
                    outbound_data.append({"路線": route, "站牌": stop_name, "方向": direction, "到站時間": stop_time})

            # 解析返程資料 (class="tteback1" 和 class="tteback2")
            for tr in soup.find_all("tr", class_=["tteback1", "tteback2"]):
                tds = tr.find_all("td")
                if len(tds) >= 4:  # 確保有足夠的 <td> 元素
                    route = tds[0].text.strip()  # 路線名稱
                    stop_name = tds[1].text.strip()  # 站牌名稱
                    direction = tds[2].text.strip()  # 去返程
                    stop_time = tds[3].get("data-deptimen1", "未知")  # 預估到站時間
                    # 如果 stop_time 是數字，轉換為分鐘數
                    if stop_time.isdigit():
                        stop_time = f"{stop_time} 分鐘後到達"
                    else:
                        stop_time = "未知"
                    inbound_data.append({"路線": route, "站牌": stop_name, "方向": direction, "到站時間": stop_time})

    # 檢查資料是否正確
    if not outbound_data:
        print("未找到去程資料，請檢查 HTML 檔案結構。")
    if not inbound_data:
        print("未找到返程資料，請檢查 HTML 檔案結構。")

    return pd.DataFrame(outbound_data), pd.DataFrame(inbound_data)

def query_bus_time(df, station_name):
    """查詢指定車站的到站時間"""
    if "站牌" not in df.columns:
        print("DataFrame 中沒有 '站牌' 欄位，請檢查資料解析邏輯。")
        return None
    result = df[df["站牌"] == station_name]
    if not result.empty:
        return result
    else:
        return None

def main():
    # 指定資料目錄
    directory = "./"  # 修改為您的 HTML 檔案所在目錄
    outbound_df, inbound_df = load_bus_data(directory)

    # 輸入車站名稱
    station_name = input("請輸入車站名稱：")

    # 查詢去程資料
    print("\n去程資料：")
    result = query_bus_time(outbound_df, station_name)
    if result is not None and not result.empty:
        print(result)
    else:
        print("未找到該車站的去程資料。")

    # 查詢返程資料
    print("\n返程資料：")
    result = query_bus_time(inbound_df, station_name)
    if result is not None and not result.empty:
        print(result)
    else:
        print("未找到該車站的返程資料。")

if __name__ == "__main__":
    main()