import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import lognorm

def plot_lognorm_cdf(mu, sigma, filename='lognorm_cdf.jpg', x_min=0.01, x_max=10, num_points=1000):
    """
    根據給定的μ與σ繪製對數常態分布的累積分布函數（CDF），並儲存為jpg檔案。

    Parameters:
        mu (float): 對數常態分布中對數值的平均值
        sigma (float): 對數常態分布中對數值的標準差
        filename (str): 儲存圖片的檔名
        x_min (float): CDF圖的X軸起始值
        x_max (float): CDF圖的X軸結束值
        num_points (int): X軸的取樣點數
    """
    x = np.linspace(x_min, x_max, num_points)
    # scipy 的 lognorm 參數是 s=σ, scale=exp(μ)
    cdf = lognorm.cdf(x, s=sigma, scale=np.exp(mu))

    plt.figure(figsize=(8, 5))
    plt.plot(x, cdf, label=f'Lognormal CDF\nμ={mu}, σ={sigma}')
    plt.title('Lognormal Cumulative Distribution Function')
    plt.xlabel('x')
    plt.ylabel('CDF')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()  # 顯示圖表
    plt.close()

# 使用函數繪製 (μ, σ) = (1.5, 0.4) 的對數常態累積分布函數圖
plot_lognorm_cdf(mu=1.5, sigma=0.4, filename='lognorm_cdf.jpg')