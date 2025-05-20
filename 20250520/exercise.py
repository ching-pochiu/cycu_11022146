import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('20250520/midterm_scores.csv')

# 設定不及格分數
passing_score = 60

# 計算每位學生不及格科目的數量
df['Fail_Count'] = (df.iloc[:, 2:] < passing_score).sum(axis=1)

# 找出超過一半科目不及格的學生
num_subjects = len(df.columns) - 2  # 扣除 Name 和 StudentID
df_failing = df[df['Fail_Count'] > num_subjects / 2]

# 顯示結果
print("超過一半科目不及格的學生：")
print(df_failing[['Name', 'StudentID', 'Fail_Count']])

# 將結果儲存為 CSV 檔案
output_path = '20250520/failing_students.csv'
df_failing[['Name', 'StudentID', 'Fail_Count']].to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"名單已儲存至 {output_path}")