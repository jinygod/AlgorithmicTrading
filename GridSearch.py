""" 변동성 돌파 전략의 k값 그리드 서치로 구하기 """
import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.model_selection import TimeSeriesSplit

def backtest_strategy(data, k):
    data = data.copy()
    data['Range'] = data['High'].shift(1) - data['Low'].shift(1)
    data.loc[:, 'Target'] = data['Close'].shift(1) + k * data['Range']
    data['Signal'] = 0

    data.loc[data['High'] > data['Target'], 'Signal'] = 1
    data.loc[data['Low'] > data['Target'], 'Signal'] = -1

    initial_balance = 100000
    balance = initial_balance
    position = 0

    for idx, row in data.iterrows():
        if row['Signal'] == 1 and position == 0:
            position = balance / row['Close']
            balance = 0
        elif row['Signal'] == -1 and position > 0:
            balance = position * row['Close']
            position = 0

    final_balance = balance + position * data.iloc[-1]['Close']
    return (final_balance / initial_balance - 1) * 100

ticker = 'LABU'
start_date = '2013-01-01'
end_date = '2023-05-03'
data = yf.download(ticker, start=start_date, end=end_date)

# k값 0.01부터 1까지 0.01씩 올려가며 그리드서치 진행
k_values = np.arange(0.01, 1.01, 0.01)
tscv = TimeSeriesSplit(n_splits=5)

best_k = None
best_performance = float('-inf')

for k in k_values:
    performances = []
    for train_index, test_index in tscv.split(data):
        train_data = data.iloc[train_index]
        test_data = data.iloc[test_index]
        performance = backtest_strategy(test_data, k)
        performances.append(performance)

    avg_performance = np.mean(performances)

    if avg_performance > best_performance:
        best_performance = avg_performance
        best_k = k

    print(f'k: {k:.2f}, Performance: {avg_performance:.2f}%')

print(f'Best k: {best_k:.2f}, Best performance: {best_performance:.2f}%')

   
