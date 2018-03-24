"""
Name: Yangfan Zhang
User ID: yzhang3067
"""
import pandas as pd
import numpy as np
import datetime as dt
import os
import sys
#import matplotlib.pyplot as plt
from util import get_data, plot_data

def get_rolling_mean(values,window):
    #Return rolling mean of given values, using window size
    return values.rolling(window).mean()

def get_rolling_std(values,window):
    #Return rolling std dev of given values, using window size
    return values.rolling(window).std()

def get_bollinger_value(values,window):
    #Return Bollinger Value
    BB = (values - get_rolling_mean(values,window))/(2*get_rolling_std(values,window))
    return BB

def get_bollinger_bands(rm,rstd):
    #Return Bollinger Bands
    upper_band = rm + rstd*2
    lower_band = rm - rstd*2
    return upper_band,lower_band

def get_momentum_value(values,window):
    #Return Momentum Value
    Momentum = (values/values.shift(window)) - 1
    return Momentum

class ManualStrategy(object):
	def __init__(self):
		self.long_entry = []
		self.short_entry = []
		
	def testPolicy(self, symbol = "AAPL", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000):
		start_date = sd
		end_date = ed
		dates = pd.date_range(start_date, end_date)
		symbols = symbol
		window = 20
		df = get_data([symbols],dates)
		df = df.fillna(method='ffill')
		df = df.fillna(method='bfill')
				
		rm = get_rolling_mean(df[symbols],window)
		rstd = get_rolling_std(df[symbols],window)
		upper_band, lower_band = get_bollinger_bands(rm,rstd)

		SMA = get_rolling_mean(df[symbols],window)
		BB = get_bollinger_value(df[symbols],window)
		Momentum = get_momentum_value(df[symbols],window)
		mom_max = Momentum.max()
		mom_min = Momentum.min()
		#print mom_max,mom_min
		
		nethold = 0
		share = []
		date = []
		position = 0 # -1,0,1 stand for short, out, long
		
		for i in range(len(upper_band.index)-1):
			if df[symbols][i-1] > upper_band.loc[upper_band.index[i-1]] and df[symbols][i] < upper_band.loc[upper_band.index[i]] and nethold != -1000:
				share.append(-1000-nethold)
				date.append(df.index[i])
				nethold = -1000
				position = -1
				self.short_entry.append(df.index[i])
				
			elif df[symbols][i-1] > rm.loc[upper_band.index[i-1]] and df[symbols][i] < rm.loc[upper_band.index[i]] and nethold == -1000:
				share.append(1000)
				date.append(df.index[i])
				nethold = 0 
				position = 0
			
			elif df[symbols][i-1] < lower_band.loc[upper_band.index[i-1]] and df[symbols][i] > lower_band.loc[upper_band.index[i]] and nethold != 1000:
				share.append(1000-nethold)
				date.append(df.index[i])
				nethold = 1000
				position = 1
				self.long_entry.append(df.index[i])
		
			elif df[symbols][i-1] < rm.loc[upper_band.index[i-1]] and df[symbols][i] > rm.loc[upper_band.index[i]] and nethold == 1000:
				share.append(-1000)
				date.append(df.index[i])
				nethold = 0
				position = 0
			
			elif Momentum.loc[upper_band.index[i]] > 0.6 and nethold != 1000:
				share.append(1000-nethold)
				date.append(df.index[i])
				nethold = 1000
				position = 1
				self.long_entry.append(df.index[i])
				
			elif Momentum.loc[upper_band.index[i]] < -0.5 and nethold != -1000:
				share.append(-1000-nethold)
				date.append(df.index[i])
				nethold = -1000
				position = -1
				self.short_entry.append(df.index[i])
			else:
				share.append(0)
				date.append(df.index[i])
				position = 0
				self.short_entry.append(df.index[i])				

		if nethold != 0:
			share.append(-nethold)
			date.append(df.index[len(df.index)-1])
		else:
			share.append(0)
			date.append(df.index[len(df.index)-1])
						
		df_trades = pd.DataFrame(data = share, index = date, columns = ['JPM'])
		#print df_trades
		return df_trades

	def benchMark(self, symbol = "AAPL", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000):
		start_date = sd
		end_date = ed
		dates = pd.date_range(start_date, end_date)
		symbols = symbol
		df = get_data([symbols],dates)
		share = [1000,-1000]
		date = [df.index[0],df.index[len(df.index)-1]]
		df_bchm = pd.DataFrame(data = share, index = date, columns = ['JPM'])
		#print df_bchm
		return df_bchm
	
def main():

	#display function for in sample data
	
	start_date = '2008-1-1'
	end_date = '2009-12-31'
	symbols = 'JPM'
    
	ms = ManualStrategy()
	df_trades = ms.testPolicy(symbols, start_date, end_date, 100000)
	port_vals = compute_portvals(orders = df_trades, start_val = 100000, commission=9.95, impact=0.005)
	df_bchm = ms.benchMark(symbols, start_date, end_date, 100000)
	port_vals_bchm = compute_portvals(orders = df_bchm, start_val = 100000, commission=9.95, impact=0.005)
	#print port_vals, port_vals_bchm

	cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(port_vals)
	cum_ret_bchm, avg_daily_ret_bchm, std_daily_ret_bchm, sharpe_ratio_bchm = compute_portfolio_stats(port_vals_bchm)

	# Compare portfolio against $SPX
	print "Date Range(In Sample): {} to {}".format(start_date, end_date)
	print
	print "In Sample Cumulative Return of Portfolio: {}".format(cum_ret)
	print "In Sample Cumulative Return of Benchmark: {}".format(cum_ret_bchm)
	print
	print "In Sample Standard Deviation of Portfolio: {}".format(std_daily_ret)
	print "In Sample Deviation of Benchmark: {}".format(std_daily_ret_bchm)
	print
	print "In Sample Average Daily Return of Portfolio: {}".format(avg_daily_ret)
	print "In Sample Average Daily Return of Benchmark: {}".format(avg_daily_ret_bchm)
	print
	print "In Sample Sharpe Ratio of Portfolio: {}".format(sharpe_ratio)
	print "In Sample Sharpe Ratio of Benchmark: {}".format(sharpe_ratio_bchm)	
	print
	print "In Sample Final Portfolio Value: {}".format(port_vals[-1])
	print "In Sample Final Benchmark Value: {}".format(port_vals_bchm[-1])
	
	port_vals_bchm_norm = port_vals_bchm / port_vals_bchm.ix[0,]
	port_vals_norm = port_vals / port_vals.ix[0,]
	port_vals_bchm_norm = port_vals_bchm_norm.to_frame()
	port_vals_norm = port_vals_norm.to_frame()
	long_entry = ms.long_entry
	short_entry = ms.short_entry
	
	f1 = plt.figure(1)
	re = port_vals_bchm_norm.join(port_vals_norm, lsuffix = '_benchmark', rsuffix = '_portfolio')
	re.columns = ['Benchmark','Value of the best possible portfolio']
	ax = re.plot(title="Normalized Benchmark and Value of The Best Possible Portfolio", fontsize=12, color = ["blue","black"])
	ax.set_xlabel("Date")
	ax.set_ylabel("Portfolio")
	ymin,ymax = ax.get_ylim()
	plt.vlines(long_entry,ymin,ymax,color='g')
	plt.vlines(short_entry,ymin,ymax,color='r')

	f2 = plt.figure(2)
	re = port_vals_bchm_norm.join(port_vals_norm, lsuffix = '_benchmark', rsuffix = '_portfolio')
	re.columns = ['Benchmark','Value of the best possible portfolio']
	ax = re.plot(title="Normalized Benchmark and Value of The Best Possible Portfolio(In Sample)", fontsize=12, color = ["blue","black"])
	ax.set_xlabel("Date")
	ax.set_ylabel("Portfolio")
	#f1.show()	

	#display function for out of sample data

	start_date = '2010-1-1'
	end_date = '2011-12-31'
	symbols = 'JPM'
    
	ms = ManualStrategy()
	df_trades = ms.testPolicy(symbols, start_date, end_date, 100000)
	port_vals = compute_portvals(orders = df_trades, start_val = 100000, commission=9.95, impact=0.005)
	df_bchm = ms.benchMark(symbols, start_date, end_date, 100000)
	port_vals_bchm = compute_portvals(orders = df_bchm, start_val = 100000, commission=9.95, impact=0.005)
	#print port_vals, port_vals_bchm

	cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(port_vals)
	cum_ret_bchm, avg_daily_ret_bchm, std_daily_ret_bchm, sharpe_ratio_bchm = compute_portfolio_stats(port_vals_bchm)

	# Compare portfolio against $SPX
	print "Date Range(Out of Sample): {} to {}".format(start_date, end_date)
	print
	print "Out of Sample Cumulative Return of Portfolio: {}".format(cum_ret)
	print "Out of Sample Cumulative Return of Benchmark: {}".format(cum_ret_bchm)
	print
	print "Out of Sample Standard Deviation of Portfolio: {}".format(std_daily_ret)
	print "Out of Sample Deviation of Benchmark: {}".format(std_daily_ret_bchm)
	print
	print "Out of Sample Average Daily Return of Portfolio: {}".format(avg_daily_ret)
	print "Out of Sample Average Daily Return of Benchmark: {}".format(avg_daily_ret_bchm)
	print
	print "Out of Sample Sharpe Ratio of Portfolio: {}".format(sharpe_ratio)
	print "Out of Sample Sharpe Ratio of Benchmark: {}".format(sharpe_ratio_bchm)	
	print
	print "Out of Sample Final Portfolio Value: {}".format(port_vals[-1])
	print "Out of Sample Final Benchmark Value: {}".format(port_vals_bchm[-1])
	
	port_vals_bchm_norm = port_vals_bchm / port_vals_bchm.ix[0,]
	port_vals_norm = port_vals / port_vals.ix[0,]
	port_vals_bchm_norm = port_vals_bchm_norm.to_frame()
	port_vals_norm = port_vals_norm.to_frame()

	f3 = plt.figure(3)
	re = port_vals_bchm_norm.join(port_vals_norm, lsuffix = '_benchmark', rsuffix = '_portfolio')
	re.columns = ['Benchmark','Value of the best possible portfolio']
	ax = re.plot(title="Normalized Benchmark and Value of The Best Possible Portfolio(Out of Sample)", fontsize=12, color = ["blue","black"])
	ax.set_xlabel("Date")
	ax.set_ylabel("Portfolio")
	#f2.show()	
	plt.show()

if __name__ == "__main__":
    main()
