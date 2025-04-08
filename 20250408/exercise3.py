import requests
import csv

def fetch_bus_info(route_id):
    """
    從臺北市公開網站抓取公車路線資料，並輸出為 CSV 格式。

    參數:
    - route_id: 公車代碼 (str)
    """
    url = f'https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}'
    response = requests.get(url)

    # 檢查 HTTP 狀態碼
    if response.status_code != 200:
        print(f"無法取得資料，HTTP 狀態碼: {response.status_code}")
        print("回應內容：")
        print(response.text)
        return

    try:
        # 解析 JSON 資料
        data = response.json()
        stops = data.get("Stops", [])

        if not stops:
            print("無法取得站點資料，請檢查公車代碼是否正確。")
            return

        result = []

        for stop in stops:
            arrival_info = stop.get('ArrivalTime', '進站中')  # 公車到達時間
            stop_number = stop.get('StopSequence', '')  # 車站序號
            stop_name = stop.get('StopName', {}).get('Zh_tw', '')  # 車站名稱 (中文)
            stop_id = stop.get('StopID', '')  # 車站編號
            latitude = stop.get('StopPosition', {}).get('PositionLat', '')  # 緯度
            longitude = stop.get('StopPosition', {}).get('PositionLon', '')  # 經度

            result.append([arrival_info, stop_number, stop_name, stop_id, latitude, longitude])

        # 輸出成 CSV 檔案
        filename = f'bus_{route_id}.csv'
        with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            # 寫入標題
            writer.writerow(["arrival_info", "stop_number", "stop_name", "stop_id", "latitude", "longitude"])
            # 寫入資料
            writer.writerows(result)

        print(f'已成功匯出 {filename}')

    except ValueError as e:
        print(f"資料解析失敗: {e}")
    except Exception as e:
        print(f"發生錯誤: {e}")

# 主程式
if __name__ == "__main__":
    route_id = input("請輸入公車代碼 (例如 '0100000A00'): ")
    fetch_bus_info(route_id)