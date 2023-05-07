import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# 데이터 다운로드
ticker = '229200.ks'
start_date = '2010-03-20'
end_date = '2023-05-07'
data = yf.download(ticker, start=start_date, end=end_date)

# 변동성 돌파 전략 파라미터
k = 0.5

# 전략에 필요한 데이터 계산
data['ATR'] = data['High'] - data['Low']
data['Range'] = data['High'].shift(1) - data['Low'].shift(1)
data['Target'] = data['Close'].shift(1) + k * data['Range']
data['Signal'] = 0

# 거래 신호 계산
data.loc[data['High'] > data['Target'], 'Signal'] = 1
data.loc[data['Low'] > data['Target'], 'Signal'] = -1

# 백테스팅
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
print("Initial balance: ", initial_balance)
print("Final balance (Volatility Breakout Strategy): ", final_balance)
print("Return (Volatility Breakout Strategy): ", (final_balance / initial_balance - 1) * 100, "%")

# 일반 매수 후 수익률 계산
initial_investment = 100000
investment_result = initial_investment * (data.iloc[-1]['Close'] / data.iloc[0]['Close'])
print("Final balance (Buy and Hold): ", investment_result)
print("Return (Buy and Hold): ", (investment_result / initial_investment - 1) * 100, "%")

# MDD 계산
cummax = data['Close'].cummax()
dd = (data['Close'] - cummax) / cummax
mdd = dd.cummin().iloc[-1]

print("Maximum Drawdown: ", mdd)

# 일반 매수 후 MDD 계산
data['max_price'] = data['Close'].cummax()
data['drawdown'] = (data['max_price'] - data['Close']) / data['max_price']
max_dd_buy_hold = data['drawdown'].max()
print("Maximum Drawdown (Buy and Hold):", max_dd_buy_hold)



# 주가 차트 및 거래 신호 표시
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label=ticker)
plt.plot(data['Close'][data['Signal'] == 1], '^', markersize=5, color='g', label='Buy')
plt.plot(data['Close'][data['Signal'] == -1], 'v', markersize=5, color='r', label='Sell')
plt.legend()
plt.show()
