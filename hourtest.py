import pandas as pd
import numpy as np
import yfinance as yf

# 데이터 다운로드
ticker = 'TQQQ'
start_date = '2023-05-01'
end_date = '2023-05-03'
data = yf.download(ticker, start=start_date, end=end_date, interval='1h')

# 변동성 돌파 전략 파라미터
k = 0.3

# 전략에 필요한 데이터 계산
data['ATR'] = data['High'] - data['Low']
data['Range'] = data['High'].shift(1) - data['Low'].shift(1)
data['Target'] = data['Close'].shift(1) + k * data['Range']
data['Signal'] = 0

# 거래 신호 계산
data.loc[data['High'] > data['Target'], 'Signal'] = 1
data.loc[data['Low'] > data['Target'], 'Signal'] = -1

# 시간 단위로 데이터 재구성
data_hourly = data.resample('1H').ffill()

# 인덱스를 datetime 형식으로 변환
data_hourly.index = pd.to_datetime(data_hourly.index)

# 백테스팅
initial_balance = 100000
balance = initial_balance
position = 0

for idx, row in data_hourly.iterrows():
    if row['Signal'] == 1 and position == 0:
        position = balance / row['Close']
        balance = 0
    elif row['Signal'] == -1 and position > 0:
        balance = position * row['Close']
        position = 0
    elif idx.time().hour in [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]:
        balance = position * row['Close']
        position = 0

final_balance_hourly = balance + position * data_hourly.iloc[-1]['Close']
print("Final balance (Volatility Breakout Strategy 1-hourly): ", final_balance_hourly)
print("Return (Volatility Breakout Strategy 1-hourly): ", (final_balance_hourly / initial_balance - 1) * 100, "%")
