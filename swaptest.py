import pandas as pd
import numpy as np
import yfinance as yf

# 데이터 다운로드
tickers = ['TQQQ', 'SQQQ']
start_date = '2000-04-01'
end_date = '2023-05-03'
data = {}
for ticker in tickers:
    data[ticker] = yf.download(ticker, start=start_date, end=end_date)

# 변동성 돌파 전략 파라미터
k = 0.30

# 전략에 필요한 데이터 계산 및 거래 신호 계산
for ticker, df in data.items():
    df['ATR'] = df['High'] - df['Low']
    df['Range'] = df['High'].shift(1) - df['Low'].shift(1)
    df['Target'] = df['Close'].shift(1) + k * df['Range']
    df['Signal'] = 0
    df.loc[df['High'] > df['Target'], 'Signal'] = 1
    df.loc[df['Low'] > df['Target'], 'Signal'] = -1

# 백테스팅
initial_balance = 100000
balance = initial_balance
position = 0

# 거래 수수료
transaction_fee = 0.0140527 / 100

for idx, row in data['TQQQ'].iterrows():
    tqqq_signal = data['TQQQ'].loc[idx, 'Signal']
    sqqq_signal = data['SQQQ'].loc[idx, 'Signal']

    if tqqq_signal == 1 and sqqq_signal != 1:
        if position == 0:
            position = balance / (data['TQQQ'].loc[idx, 'Close'] * (1 + transaction_fee))
            balance = 0
            current_ticker = 'TQQQ'
    elif sqqq_signal == 1 and tqqq_signal != 1:
        if position == 0:
            position = balance / (data['SQQQ'].loc[idx, 'Close'] * (1 + transaction_fee))
            balance = 0
            current_ticker = 'SQQQ'
    elif tqqq_signal == -1 or sqqq_signal == -1:
        if position > 0:
            balance = position * (data[current_ticker].loc[idx, 'Close'] * (1 - transaction_fee))
            position = 0

final_balance = balance + position * data[current_ticker].iloc[-1]['Close']
print("Initial balance: ", initial_balance)
print("Final balance (Volatility Breakout Strategy): ", final_balance)
print("Return (Volatility Breakout Strategy): ", (final_balance / initial_balance - 1) * 100, "%")
