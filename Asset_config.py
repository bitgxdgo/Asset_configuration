import pandas as pd
import numpy as np
import os
from scipy.optimize import minimize

def clean_percentage_data(value):
    """清理百分比数据"""
    if isinstance(value, str):
        return float(value.strip('%')) / 100
    return value

def calculate_portfolio_parameters(directory_path, max_days=500):
    """计算投资组合所需的参数：年化收益率、波动率和协方差矩阵"""
    daily_returns_dict = {}
    annual_returns = {}
    annual_volatility = {}
    
    for file in os.listdir(directory_path):
        if file.endswith('.csv'):
            df = pd.read_csv(os.path.join(directory_path, file))
            df['w782'] = pd.to_datetime(df['w782'])
            df['tor (3)'] = df['tor (3)'].apply(clean_percentage_data)
            df = df.sort_values('w782', ascending=False)
            df = df.head(max_days)
            
            asset_name = file.replace('.csv', '')
            daily_returns = df['tor (3)'].values
            daily_returns_dict[asset_name] = daily_returns
            
            avg_daily_return = daily_returns.mean()
            annual_returns[asset_name] = avg_daily_return * 250
            
            daily_volatility = daily_returns.std()
            annual_volatility[asset_name] = daily_volatility * np.sqrt(250)
    
    daily_returns_df = pd.DataFrame(daily_returns_dict)
    covariance_matrix = daily_returns_df.cov() * 250
    
    return annual_returns, annual_volatility, covariance_matrix

def optimize_portfolio(returns, cov_matrix, target_return, allow_short=False):
    """优化投资组合以最小化风险"""
    assets = list(returns.keys())
    n = len(assets)
    r = np.array([returns[asset] for asset in assets])
    
    def portfolio_variance(weights):
        return np.dot(weights.T, np.dot(cov_matrix, weights))
    
    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
        {'type': 'eq', 'fun': lambda w: np.dot(w, r) - target_return}
    ]
    
    bounds = [(0, 1) if not allow_short else (-1, 1) for _ in range(n)]
    initial_weights = np.array([1/n] * n)
    
    result = minimize(portfolio_variance, 
                      initial_weights,
                      method='SLSQP',
                      bounds=bounds,
                      constraints=constraints)
    
    return dict(zip(assets, result.x))

# 主程序
directory_path = "/Users/Zhuanz1/Asset_configuration"
target_annual_return = 0.1 # 目标年化收益率为10%
total_capital = 800000  # 总资本80万元

# 计算年化收益率、波动率和协方差矩阵
annual_returns, annual_volatility, covariance_matrix = calculate_portfolio_parameters(directory_path)

# 打印各资产的年化指标
print("各资产的年化指标：")
for asset in annual_returns.keys():
    print(f"\n{asset}:")
    print(f"年化收益率: {annual_returns[asset]:.2%}")
    print(f"年化波动率: {annual_volatility[asset]:.2%}")

print("\n" + "="*50 + "\n")

# 优化投资组合
optimal_weights = optimize_portfolio(annual_returns, covariance_matrix, target_annual_return)

# 打印最优配置结果
print("最优资产配置方案：")
print(f"总投资金额：{total_capital:,.0f}元")
print("\n资产配置明细：")
for asset, weight in optimal_weights.items():
    amount = weight * total_capital
    print(f"{asset}:")
    print(f"  配置比例: {weight:.2%}")
    print(f"  配置金额: {amount:,.0f}元")