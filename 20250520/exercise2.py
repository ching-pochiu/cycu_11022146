import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 讀取成績資料
file_path = "C:/Users/User/Desktop/cycu_11022146/20250520/midterm_scores.csv"
data = pd.read_csv(file_path)

# 定義分數區間
bins = np.arange(0, 101, 10)  # 每 10 分一區間
bin_labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins) - 1)]

# 計算每個科目在每個分數區間的分布
subject_columns = data.columns[2:]  # 取得所有科目名稱
histograms = {subject: np.histogram(data[subject], bins=bins)[0] for subject in subject_columns}

# 繪製長條圖
x = np.arange(len(bin_labels))  # 分數區間的 x 軸位置
bar_width = 0.1  # 每個長條的寬度
colors = plt.cm.tab20.colors  # 使用多種顏色

plt.figure(figsize=(12, 8))
for i, subject in enumerate(subject_columns):
    plt.bar(x + i * bar_width, histograms[subject], width=bar_width, label=subject, color=colors[i % len(colors)])

# 設定圖表標題與軸標籤
plt.title('Score Distribution by Subject and Range', fontsize=16)
plt.xlabel('Score Range', fontsize=12)
plt.ylabel('Number of Students', fontsize=12)
plt.xticks(x + bar_width * (len(subject_columns) - 1) / 2, bin_labels, rotation=45)
plt.legend(title="Subjects")
plt.tight_layout()

# 儲存圖表
chart_file = "C:/Users/User/Desktop/cycu_11022146/20250520/subject_score_range_distribution_chart.png"
plt.savefig(chart_file)
plt.show()
print(f"分數區間內各科目成績分布長條圖已儲存至 {chart_file}")