import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def plot_normal_distribution(mu, sigma, output_filename="normal_distribution.jpg"):
    """
    繪製常態分布的機率密度函數 (PDF) 並儲存為 JPG 圖檔。

    參數:
    mu (float): 常態分布的平均值 (μ)。
    sigma (float): 常態分布的標準差 (σ)。
    output_filename (str): 儲存的 JPG 檔案名稱 (預設為 "normal_distribution.jpg")。
    """
    # 定義 x 軸範圍
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)
    # 計算 PDF 值
    y = norm.pdf(x, mu, sigma)

    # 繪製圖形
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f"μ={mu}, σ={sigma}", color="blue")
    plt.title("Normal Distribution PDF")
    plt.xlabel("x")
    plt.ylabel("Probability Density")
    plt.legend()
    plt.grid(True)

    # 儲存為 JPG 圖檔
    plt.savefig(output_filename, format="jpg")
    plt.close()
    print(f"圖形已儲存為 {output_filename}")

# 範例使用
# plot_normal_distribution(0, 1)  # 繪製標準常態分布
plot_normal_distribution(0, 1, "C:/Users/domi1/OneDrive/桌面/normal_distribution.jpg")

