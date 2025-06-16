from datetime import datetime

def analyze_date_time(input_time):
    """
    分析輸入的時間字串，完成以下任務：
    1. 回傳該日期為星期幾。
    2. 回傳該日期是當年的第幾天。
    3. 計算從該時刻到現在時間，共經過了幾個太陽日 (Julian date)。

    參數:
    input_time (str): 時間字串，格式為 "YYYY-MM-DD HH:MM"。

    回傳:
    tuple: (星期幾, 當年的第幾天, 經過的太陽日)
    """
    # 解析輸入的時間字串
    input_datetime = datetime.strptime(input_time, "%Y-%m-%d %H:%M")
    
    # 1. 回傳該日期為星期幾
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekdays[input_datetime.weekday()]
    
    # 2. 回傳該日期是當年的第幾天
    day_of_year = input_datetime.timetuple().tm_yday
    
    # 3. 計算從該時刻到現在時間，共經過了幾個太陽日
    now = datetime.now()
    delta = now - input_datetime
    julian_days = delta.total_seconds() / 86400  # 1 太陽日 = 86400 秒
    
    return weekday, day_of_year, julian_days

# 使用者輸入時間
input_time = input("請輸入時間 (格式: YYYY-MM-DD HH:MM): ")
try:
    result = analyze_date_time(input_time)
    print(f"日期為: {result[0]}")
    print(f"當年的第幾天: {result[1]}")
    print(f"經過的太陽日: {result[2]:.2f}")
except ValueError:
    print("輸入的時間格式不正確，請使用 YYYY-MM-DD HH:MM 格式。")