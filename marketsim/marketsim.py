"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
	df = pd.read_csv(orders_file, index_col = 'Date', parse_dates = True, na_values = ['nan'])

	start_date = min(df.index)
	end_date = max(df.index)

	symbols = []
	for i, row in df.iterrows():
		if row['Symbol'] not in symbols:
			symbols.append(row['Symbol'])
	#print symbols
    
	prices_symbol = get_data(symbols, pd.date_range(start_date, end_date))
    
	for symbol in symbols:
		prices_symbol[symbol + ' Shares'] = pd.Series(0, index=prices_symbol.index)
		prices_symbol['Port Val'] = pd.Series(start_val, index=prices_symbol.index)
		prices_symbol['Cash'] = pd.Series(start_val, index=prices_symbol.index)
	#print prices_symbol
	
	for i, row in df.iterrows():
		symbol = row['Symbol']
		if row['Order'] == 'BUY':
			prices_symbol.ix[i:, symbol + ' Shares'] = prices_symbol.ix[i:, symbol + ' Shares'] + row['Shares']
			prices_symbol.ix[i:, 'Cash'] -= prices_symbol.ix[i, symbol] * row['Shares'] * (1+impact) + commission
		if row['Order'] == 'SELL':
			prices_symbol.ix[i:, symbol + ' Shares'] = prices_symbol.ix[i:, symbol + ' Shares'] - row['Shares']
			prices_symbol.ix[i:, 'Cash'] += prices_symbol.ix[i, symbol] * row['Shares'] * (1-impact) - commission
	#print prices_symbol
	
	for i, row in prices_symbol.iterrows():
		shares_val = 0
		for symbol in symbols:
			shares_val += prices_symbol.ix[i, symbol + ' Shares'] * row[symbol]
			prices_symbol.ix[i, 'Port Val'] = prices_symbol.ix[i, 'Cash'] + shares_val
	#print prices_symbol.ix[:, 'Port Val']

	return prices_symbol.ix[:, 'Port Val']

def author():
	return 'yzhang3067'

def compute_portfolio(allocs, prices, sv = 1):
    normed = prices / prices.ix[0,]
    alloced = normed * allocs
    pos_vals = alloced * sv
    port_val = pos_vals.sum(axis = 1)
    return port_val
    
def compute_portfolio_stats(port_val):
    daily_ret = (port_val/port_val.shift(1)) - 1   
    cr = (port_val[-1]/port_val[0]) - 1
    adr = daily_ret.mean()
    sddr = daily_ret.std()
    sr = np.sqrt(252.0) * ((daily_ret - 0.0).mean() / sddr)
    return cr, adr, sddr, sr

def test_code():
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    #of = "./orders2.csv"
    of = "./orders.csv"
    #of = "./orders-short.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file = of, start_val = sv)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]] # just get the first column
    else:
        "warning, code did not return a DataFrame"

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    #start_date = dt.datetime(2011,1,10)
    #end_date = dt.datetime(2011,12,20)
    df = pd.read_csv(of, index_col = 'Date', parse_dates = True, na_values = ['nan'])
    start_date = min(df.index)
    end_date = max(df.index)
    prices_SPX = get_data(['$SPX'], pd.date_range(start_date, end_date))
    prices_SPX = prices_SPX[['$SPX']]
    portvals_SPX = compute_portfolio([1.0], prices_SPX)
    cum_ret_SPX, avg_daily_ret_SPX, std_daily_ret_SPX, sharpe_ratio_SPX = compute_portfolio_stats(portvals_SPX)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(portvals)

    # Compare portfolio against $SPX
    print "Date Range: {} to {}".format(start_date, end_date)
    print
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)
    print "Sharpe Ratio of $SPX : {}".format(sharpe_ratio_SPX)
    print
    print "Cumulative Return of Fund: {}".format(cum_ret)
    print "Cumulative Return of $SPX : {}".format(cum_ret_SPX)
    print
    print "Standard Deviation of Fund: {}".format(std_daily_ret)
    print "Standard Deviation of $SPX : {}".format(std_daily_ret_SPX)
    print
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)
    print "Average Daily Return of $SPX : {}".format(avg_daily_ret_SPX)
    print
    print "Final Portfolio Value: {}".format(portvals[-1])

if __name__ == "__main__":
    test_code()
