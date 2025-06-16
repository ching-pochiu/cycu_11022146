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

# Math scores
math_scores = df['Math']

# Define bins: 0-9, 10-19, ..., 90-100
bins = [0,10,20,30,40,50,60,70,80,90,100]
labels = [f"{bins[i]}-{bins[i+1]-1}" for i in range(len(bins)-1)]
# Plot histogram
plt.hist(math_scores, bins=bins, edgecolor='black', rwidth=0.8)

plt.xlabel('Math Score Range')
plt.ylabel('Number of Students')
plt.title('Distribution of Math Scores')
plt.xticks(bins, rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()