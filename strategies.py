import backtrader as bt

# Create a simple price printing Stratey
class PrintTickPrices(bt.Strategy):

    def log(self, txt, dt=None):
        # Logging function for this strategy
        dt = dt or self.datas[0].datetime.datetime(0) 
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "low and high" lines in the data[0] dataseries
        self.databid = self.datas[0].low
        self.dataask = self.datas[0].high
        

    def next(self):
        # Log the price of the series from the reference
        self.log('Bid, %.5f' % self.databid[0])
        self.log('Ask, %.5f' % self.dataask[0])
        # input('hit enter')


class PrintBarPrices(bt.Strategy):
    
    def log(self, txt, dt=None):
        # Logging function for this strategy
        dt = dt or self.datas[0].datetime.datetime(0) 
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "low and high" lines in the data[0] dataseries
        self.datalow = self.datas[0].low
        self.datahigh = self.datas[0].high
        

    def next(self):
        # Log the price of the series from the reference
        self.log('Low, %.5f' % self.datalow[0])
        self.log('High, %.5f' % self.datahigh[0])
        input('hit enter')
