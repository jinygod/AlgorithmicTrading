import backtrader as bt
import pandas as pd
import numpy as np

# 랜덤 데이터 생성
data = pd.DataFrame(np.random.randint(100, 200, size=(100, 5)),
                    columns=['Open', 'High', 'Low', 'Close', 'Volume'],
                    index=pd.date_range(start='2022-01-01', periods=100, freq='D'))

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.data_close = self.datas[0].close
        self.order = None

    def next(self):
        if not self.position:
            if self.data_close[0] > self.data_close[-1]:
                if self.data_close[-1] > self.data_close[-2]:
                    self.buy(size=100)
        elif self.data_close[0] < self.data_close[-1]:
            self.close()

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.001)

    data = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data)

    cerebro.addstrategy(MyStrategy)
    cerebro.run()
    print(f"종료 후 계좌 잔고: {cerebro.broker.getvalue():,.0f} 원")
