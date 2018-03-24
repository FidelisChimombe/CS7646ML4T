"""
Name: Yangfan Zhang
User ID: yzhang3067
"""
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(orders_df, start_val = 1000000, commission=9.95, impact=0.005):
    symbols = orders_df.columns.values.tolist()
    
    n = len(orders_df)
    date_list = orders_df.index.tolist()
    start_date = date_list[0]
    end_date = date_list[n - 1]
    orders_df.insert(loc=1,column='Date',value=date_list)
    orders_df.columns = ['Order', 'Date']
    
    # get stock price data and cancel SPY
    stock_price = get_data(symbols, pd.date_range(start_date, end_date))
    stock_price = stock_price[symbols]
    # portfolio init
    owner_port = dict.fromkeys(symbols,0)
    cash = start_val
        

    daily_port = pd.DataFrame(index=stock_price.index)
    daily_port.insert(loc=0, column='Daily Portfolio', value = np.zeros(len(daily_port.index)))

    # Bench Mark
    daily_bench = pd.DataFrame(index=stock_price.index)
    daily_bench.insert(loc=0, column='Daily Portfolio', value = np.zeros(len(daily_port.index)))
    bench_port = dict.fromkeys(symbols,1000)
    cash_bench = 100000 - stock_price.ix[0]['JPM'] * 1000
   
    # Signal for manual strategy
    signal = pd.DataFrame(index=stock_price.index)
    signal.insert(loc=0, column='Operations', value = np.zeros(len(daily_port.index)))

    for date, price in stock_price.iterrows():        
        for index, order in orders_df[ orders_df['Date'] == str(date.date())].iterrows():
            owner_port["JPM"] += order.Order
            if order.Order > 0:
		signal.ix[str(date.date())] = 1
	    elif order.Order < 0:
 		signal.ix[str(date.date())] = -1
            cash -= (1+impact) * stock_price.ix[order.Date]['JPM'] * order.Order
    	    cash -= commission
    	portvals = cash
        for stock, shares in owner_port.iteritems():
	     portvals = portvals + stock_price.ix[date][stock] * shares
        daily_port.ix[str(date.date())] = portvals
        daily_bench.ix[date] = cash_bench + stock_price.ix[date]["JPM"] * 1000
        
    
    # Cumulative return, Stdev of daily returns, Mean of daily return 
    
    daily_rets = ( daily_port / daily_port.shift(1)) - 1
    cr = (daily_port.iloc[-1,0] / daily_port.iloc[0,0]) - 1
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    print "Cumulative Return of JPM: {}".format(cr)
    print "Standard Deviation of JPM: {}".format(sddr)     
    print "Average Daily Return of JPM: {}".format(adr)
  
    # For bench mark
    bench_rets = ( daily_bench / daily_bench.shift(1)) - 1
    cr_bm = (daily_bench.iloc[-1,0] / daily_bench.iloc[0,0]) - 1
    adr_bm = bench_rets.mean()
    sddr_bm = bench_rets.std()
    print "Cumulative Return of Benchmark: {}".format(cr_bm)
    print "Standard Deviation of Benchmark: {}".format(sddr_bm)
    print "Average Daily Return of Benchmark: {}".format(adr_bm)
 
    return daily_port, daily_bench, signal

def author():
	return 'yzhang3067'

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders2.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"
    
    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    start_date = dt.datetime(2008,1,1)
    end_date = dt.datetime(2008,6,1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
