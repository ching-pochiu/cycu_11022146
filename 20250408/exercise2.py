from datetime import datetime

def calculate_julian_and_weekday(input_time):
    # 將輸入的時間字串轉換為 datetime 物件
    input_format = "%Y-%m-%d %H:%M"
    input_datetime = datetime.strptime(input_time, input_format)

    # 計算該天是星期幾
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekdays[input_datetime.weekday()]

    # 計算 Julian 日期
    julian_start = datetime(4713, 1, 1, 12)  # Julian 日期的起始點
    delta = input_datetime - julian_start
    julian_date = 2400000.5 + delta.days + delta.seconds / 86400  # Julian 日期

    # 計算該時刻至今經過的太陽日
    now = datetime.now()
    delta_now = now - input_datetime
    elapsed_days = delta_now.days + delta_now.seconds / 86400  # 浮點數表示

    return weekday, julian_date, elapsed_days

# 主程式
if __name__ == "__main__":
    # 提示使用者輸入時間
    input_time = input("請輸入時間（格式為 YYYY-MM-DD HH:MM，例如 2020-04-15 20:30）：")
    try:
        # 計算結果
        weekday, julian_date, elapsed_days = calculate_julian_and_weekday(input_time)

        # 輸出結果
        print(f"輸入時間為：{input_time}")
        print(f"該天是：{weekday}")
        print(f"該時刻的 Julian 日期為：{julian_date}")
        print(f"該時刻至今經過的太陽日數為：{elapsed_days}")
    except ValueError:
        print("輸入的時間格式不正確，請使用 YYYY-MM-DD HH:MM 格式。")