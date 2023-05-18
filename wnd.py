import cryptocompare
import pandas as pd
import backtrader as bt
import numpy as np
import datetime

# 데이터를 가져오는 부분
df = cryptocompare.get_historical_price_day('BTC', currency='USD', limit=365, toTs=datetime.datetime.now())
df = pd.DataFrame(df)
df['time'] = pd.to_datetime(df['time'], unit='s')
df.set_index('time', inplace=True, drop=False)
df = df[['open', 'high', 'low', 'close', 'volumeto']]

# Backtrader에서 사용할 수 있는 Pandas 데이터 형식을 정의합니다.
class PandasData(bt.feeds.PandasData):
    lines = ('open', 'high', 'low', 'close', 'volumeto',)
    params = (
        ('datetime', None),
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volumeto', -1),
    )

# 워뇨띠 매매법에 따른 거래 전략을 정의합니다.
class MyStrategy(bt.Strategy):
    params = (('quantity', 1),)

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.datavolume = self.datas[0].volumeto

    def next(self):
        # 거래량이 급증하는 경우 매수합니다.
        if self.datavolume[-1] > np.mean(self.datavolume.get(size=5)):
            self.buy(size=self.params.quantity)

        # 가격이 하락하면 매도합니다.
        if self.dataclose[-1] < self.dataclose[-2]:
            self.sell(size=self.params.quantity)

if __name__ == '__main__':
    # 초기 자본 설정
    initial_cash = 100000000  # 1억 원

    cerebro = bt.Cerebro()
    cerebro.addstrategy(MyStrategy)
    cerebro.broker.setcash(initial_cash)

    # 데이터를 불러옵니다.
    data = PandasData(dataname=df)
    cerebro.adddata(data)

    # 초기 포트폴리오 가치를 출력합니다.
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    # 최종 포트폴리오 가치를 출력합니다.
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
