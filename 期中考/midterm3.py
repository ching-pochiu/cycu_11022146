import requests
import csv

def fetch_bus_route_data(route_id, output_filename="bus_route_data.csv"):
    """
    從台北市公車公開 API 爬取資料並輸出為 CSV 檔案。

    參數:
    route_id (str): 公車路線代碼。
    output_filename (str): 輸出的 CSV 檔案名稱 (預設為 "bus_route_data.csv")。
    """
    # API URL
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    
    try:
        # 發送 GET 請求
        response = requests.get(url)
        response.raise_for_status()  # 檢查請求是否成功
        data = response.json()  # 解析 JSON 資料

        # 檢查資料是否存在
        if not data or "Stops" not in data:
            print("無法取得資料，請檢查路線代碼是否正確。")
            return

        # 解析資料
        stops = data["Stops"]
        rows = []
        for stop in stops:
            stop_number = stop.get("StopSequence", "")
            stop_name = stop.get("StopName", {}).get("Zh_tw", "")
            stop_id = stop.get("StopID", "")
            latitude = stop.get("StopPosition", {}).get("PositionLat", "")
            longitude = stop.get("StopPosition", {}).get("PositionLon", "")
            rows.append([route_id, stop_number, stop_name, stop_id, latitude, longitude])

        # 將資料寫入 CSV 檔案
        with open(output_filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            # 寫入欄位名稱
            writer.writerow(["公車路線代碼", "車站序號", "車站名稱", "車站編號", "latitude", "longitude"])
            # 寫入資料
            writer.writerows(rows)

        print(f"資料已成功儲存至 {output_filename}")

    except requests.exceptions.RequestException as e:
        print(f"無法取得資料，請檢查網路連線或路線代碼是否正確。錯誤訊息: {e}")
    except Exception as e:
        print(f"發生錯誤: {e}")

# 範例使用
route_id = input("請輸入公車路線代碼: ")
fetch_bus_route_data(route_id, "bus_route_data.csv")