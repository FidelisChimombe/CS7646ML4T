"""MC2-P1: Market simulator."""

import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def compute_portvals(orders, start_val = 1000000, commission=9.95, impact=0.005):
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
	#df = pd.read_csv(orders_file, index_col = 'Date', parse_dates = True, na_values = ['nan'])
	df = formatchange(orders)
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

def formatchange(df):
	symbol = []
	order = []
	share = []
	for i in range(len(df.index)):
		symbol.append('JPM')
		if df['orders'][i] > 0:
			order.append('BUY')
			share.append(df['orders'][i])			
		elif df['orders'][i] < 0:
			order.append('SELL')	
			share.append(-df['orders'][i])
	df_symbol = pd.DataFrame(data = symbol, index = df.index, columns = ['Symbol'])			
	df_order = pd.DataFrame(data = order, index = df.index, columns = ['Order'])	
	df_share = pd.DataFrame(data = share, index = df.index, columns = ['Shares'])	

	df_result = df_symbol.join(df_order).join(df_share)
	#print df_result
	
	return df_result
	
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
