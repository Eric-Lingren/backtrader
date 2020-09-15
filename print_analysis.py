def printTradeSummary(analyzer):

    #Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total,2)
    strike_rate = (total_won / total_closed) * 100
    strike_rate = round(strike_rate, 2)
    pnl_average = round(analyzer.pnl.net.average, 2)

    #Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate','Win Streak', 'Losing Streak', 'PnL Net']
    h3 = ['PnL Average', '', '', '']
    r1 = [total_open, total_closed,total_won,total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    r3 = [pnl_average, '', '', '']

    #Print the rows
    print_list = [h1,r1,h2,r2,h3,r3]
    row_format ="{:<20}" * (5)
    print("Trade Analysis Results:\n")
    for row in print_list:
        print(row_format.format('',*row))



def printSystemDrawdown(analyzer):

    max_drawdown_percent = round(analyzer.max.drawdown, 2)
    max_drawdown_amount = round(analyzer.max.moneydown, 2)
    trade_drawdown_percent = round(analyzer.drawdown, 2)
    trade_drawdown_amount = round(analyzer.moneydown, 2)

    #Designate the rows
    h1 = ['Max Drawdown %', 'Max Drawdown $', 'Trade Drawdown %', 'Trade Drawdown $']
    r1 = [max_drawdown_percent, max_drawdown_amount, trade_drawdown_percent, trade_drawdown_amount]


    #Print the rows
    print_list = [h1,r1]
    row_format ="{:<20}" * (5)
    print("\nSystem Drawdown Results:\n")
    for row in print_list:
        print(row_format.format('',*row))



def printSystemSharp(analyzer):

    sharp_ratio = round(analyzer['sharperatio'], 4)

    #Designate the rows
    h1 = ['Sharp Ratio', '', '', '']
    r1 = [sharp_ratio, '', '', '']

    #Print the rows
    print_list = [h1,r1]
    row_format ="{:<20}" * (5)
    print("\nSystem Sharp Ratio:\n")
    for row in print_list:
        print(row_format.format('',*row))

    
