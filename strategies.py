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
        # self.datalow = self.datas[0].low
        # self.datahigh = self.datas[0].high
        self.dataclose = self.datas[0].close
        
    def next(self):
        # Log the price of the series from the reference
        # self.log('Low, %.5f' % self.datalow[0])
        # self.log('High, %.5f' % self.datahigh[0])
        self.log('Close, %.5f' % self.dataclose[0])
        # input('hit enter')




class FallingClosePrices(bt.Strategy):
    
    def log(self, txt, dt=None):
        # Logging function for this strategy
        dt = dt or self.datas[0].datetime.datetime(0) 
        print('%s, %s' % (dt.isoformat(), txt))


    def __init__(self):
        self.dataclose = self.datas[0].close
        # To keep track of pending orders
        self.order = None


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
        # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.5f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.5f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None
        

    def next(self):
        self.log('Close, %.5f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] < self.dataclose[-1]:
                    # current close less than previous close

                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close

                    # BUY, BUY, BUY!!! (with default parameters)
                    self.log('BUY CREATE, %.5f' % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.buy()

        else:

            # Already in the market ... we might sell
            if len(self) >= (self.bar_executed + 50):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.5f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()




class MovingAverageTest(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.maperiod)

        # Indicators for the plotting show
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25).subplot = True
        # bt.indicators.StochasticSlow(self.datas[0])
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0]).plot = False

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.5f, Cost: %.5f, Comm %.5f' %
                    (order.executed.price,
                    order.executed.value,
                    order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.5f, Cost: %.5f, Comm %.5f' %
                        (order.executed.price,
                        order.executed.value,
                        order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.5f, NET %.5f' %
                (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.5f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] > self.sma[0]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                self.log('BUY CREATE, %.5f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:

            if self.dataclose[0] < self.sma[0]:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.5f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()




class RSITest(bt.Strategy):
    params = (
        ('profit_target', 10),
        ('loss_target', 10),
        ('rsiperiod1', 21),
        ('rsi_limit', 70),
        ('momentumperiod', 20 )
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        date = dt or self.datas[0].datetime.date(0)
        time = dt or self.datas[0].datetime.time(0)
        # print('%s %s - %s' % (date.isoformat(), time, txt))

    def __init__(self):
        print('---------- Running RSI Test Stratgey ----------\n')
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datahigh = self.datas[0].high
        

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add indicators
        self.rsi = bt.indicators.RSI(
            self.datas[0], period=self.params.rsiperiod1)

        self.momentum = bt.indicators.Momentum(
            self.datas[0], period=self.params.momentumperiod)

        # Indicators for the plotting show
        # rsi = bt.indicators.RSI(self.datas[0])


    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():                
                self.log(
                    'BUY EXECUTED, Price: %.5f, Cost: %.5f, Comm %.5f' %
                    (order.executed.price,
                    order.executed.value,
                    order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            self.bar_executed = len(self)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None


    def notify_trade(self, trade):
        if trade.isclosed:
            self.log( 'OPERATION PROFIT, GROSS %.5f, NET %.5f' % (trade.pnl, trade.pnlcomm) )


    def next(self):
        # If an order is pending, break function since we cant send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Check Buy
            if self.rsi[0] < 30:
                if (self.dataclose[-2] >= self.dataclose[-1]) and (self.dataclose[-1] >= self.dataclose[0]):
                    self.order = self.buy()
                    self.log('New BUY CREATE, %.5f' % self.dataclose[0])
            #     for index in range(6):
            #         print(self.momentum[-index])
            #     # if self.datahigh[0] > self.datahigh[-4]:
            #     # if self.momentum[0] > self.momentum[-4]:
            #         # Keep track of the created order to avoid a 2nd order
            #     self.order = self.buy()
            #     self.log('BUY CREATE, %.5f' % self.dataclose[0])
            # Check Sell 
            if self.rsi[0] > self.params.rsi_limit:
                if (self.dataclose[-2] <= self.dataclose[-1]) and (self.dataclose[-1] <= self.dataclose[0]):

                # if (self.momentum[-2] >= self.momentum[-1]) and (self.momentum[-1] >= self.momentum[0]):
                #     print('lower Momemtums')
                    self.order = self.sell()
                    self.log('New Sell CREATE, %.5f' % self.dataclose[0])

        else:
            order_value = self.position.price*self.position.size
            current_value = self.dataclose[0]*self.position.size

            if (current_value - order_value > self.params.profit_target) or (current_value - order_value < -self.params.loss_target):
                self.log('Closing order, %.5f' % self.dataclose[0])
                self.order = self.close()

    # Used for optimizations only
    # def stop(self):
    #     print('(Profit Target of %2d) Ending Value %.2f' %
    #             (self.params.loss_target, self.broker.getvalue()))
    #     print('(loss Target of %2d) Ending Value %.2f' %
    #             (self.params.loss_target, self.broker.getvalue()))
        # print('(RSI Limit of of %2d) Ending Value %.2f' %
        #         (self.params.rsi_limit, self.broker.getvalue()))
