import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 設定支援中文的字體
rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體
rcParams['axes.unicode_minus'] = False  # 解決負號無法顯示的問題

# 讀取 CSV 並繪製折線圖（買入與賣出的現金匯率）
def read_csv_and_plot_cash_rates(file_path):
    try:
        # 使用 pandas 讀取 CSV 檔案，指定編碼為 big5
        data = pd.read_csv(file_path, encoding='big5', delimiter='\t')
        
        # 修正欄位名稱
        data.columns = ['資料日期', '幣別', '匯率類型1', '買入現金匯率', '匯率類型2', '賣出現金匯率']
        
        # 過濾掉非日期的行，確保 '資料日期' 欄位只包含有效日期
        data = data[pd.to_numeric(data['資料日期'], errors='coerce').notna()]
        
        # 選取需要的欄位
        data = data[['資料日期', '買入現金匯率', '賣出現金匯率']].dropna()
        
        # 將 '資料日期' 轉換為日期格式
        data['資料日期'] = pd.to_datetime(data['資料日期'], format='%Y%m%d')
        
        # 繪製折線圖
        plt.figure(figsize=(14, 7))  # 調整圖表大小
        plt.plot(data['資料日期'], data['賣出現金匯率'], label='賣出現金匯率', color='blue', linewidth=2)  # 紅色線
        plt.plot(data['資料日期'], data['買入現金匯率'], label='買入現金匯率', color='red', linewidth=2)  # 藍色線
        
        # 設定圖表標題與標籤
        plt.title('現金匯率走勢圖', fontsize=18, fontweight='bold')
        plt.xlabel('日期', fontsize=14)
        plt.ylabel('匯率', fontsize=14)
        
        # 調整圖例位置與樣式
        plt.legend(loc='upper left', fontsize=12)
        
        # 增加網格線
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        
        # 調整 X 軸日期標籤
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        
        # 自動調整佈局
        plt.tight_layout()
        
        # 顯示圖表
        plt.show()
    except Exception as e:
        print(f"發生錯誤：{e}")

# 範例使用
file_path = r'C:\Users\User\Desktop\cycu_11022146\ExchangeRate@202503251849.csv'
read_csv_and_plot_cash_rates(file_path)