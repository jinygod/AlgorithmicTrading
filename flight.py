import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# 데이터 다운로드
ticker = 'TQQQ'
start_date = '2023-03-20'
end_date = '2023-05-03'
data = yf.download(ticker, start=start_date, end=end_date, interval='1d')

# 플라이트 매매법 파라미터
n = 20
k = 2

# 전략에 필요한 데이터 계산
data['MA'] = data['Close'].rolling(n).mean()
data['STD'] = data['Close'].rolling(n).std()
data['Upper'] = data['MA'] + k * data['STD']
data['Lower'] = data['MA'] - k * data['STD']
data['Signal'] = 0

# 거래 신호 계산
data.loc[data['Close'] > data['Upper'], 'Signal'] = -1
data.loc[data['Close'] < data['Lower'], 'Signal'] = 1

# 백테스팅
initial_balance = 100000
balance = initial_balance
position = 0
max_balance = initial_balance
max_drawdown = 0

for idx, row in data.iterrows():
    if row['Signal'] == 1 and position == 0:
        position = balance / row['Close']
        balance = 0
    elif row['Signal'] == -1 and position > 0:
        balance = position * row['Close']
        position = 0
    if balance + position * row['Close'] > max_balance:
        max_balance = balance + position * row['Close']
    drawdown = 1 - (balance + position * row['Close']) / max_balance
    if drawdown > max_drawdown:
        max_drawdown = drawdown

final_balance = balance + position * data.iloc[-1]['Close']
print("Initial balance: ", initial_balance)
print("Final balance (Fly-to-Quality Strategy): ", final_balance)
print("Return (Fly-to-Quality Strategy): ", (final_balance / initial_balance - 1) * 100, "%")
print("Max Drawdown (Fly-to-Quality Strategy): ", max_drawdown * 100, "%")

# 주가 차트 및 거래 신호 표시
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label=ticker)
plt.plot(data['Upper'], '--', color='red', label='Upper')
plt.plot(data['MA'], '--', color='black', label='MA')
plt.plot(data['Lower'], '--', color='blue', label='Lower')
