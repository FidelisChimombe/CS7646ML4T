import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
from util import get_data, plot_data
from marketsimcode import compute_portvals, compute_portfolio, compute_portfolio_stats, formatchange

class BestPossibleStrategy(object):

	def testPolicy(self, symbol = "AAPL", sd=dt.datetime(2010,1,1), ed=dt.datetime(2011,12,31), sv = 100000):
		start_date = sd
		end_date = ed
		dates = pd.date_range(start_date, end_date)
		symbols = symbol
		df = get_data([symbols],dates)
		df = df.fillna(method='ffill')
		df = df.fillna(method='bfill')
		
		nethold = 0
		share = []
		date = []
		for i in range(len(df.index)-1):
			if df[symbols][i] < df[symbols][i+1] and nethold == 0:
				share.append(1000)
				date.append(df.index[i])
				nethold += 1000
			elif df[symbols][i] < df[symbols][i+1] and nethold == -1000:
				share.append(2000)
				date.append(df.index[i])
				nethold += 2000
			elif df[symbols][i] > df[symbols][i+1] and nethold == 0:
				share.append(-1000)
				date.append(df.index[i])
				nethold += -1000
			elif df[symbols][i] > df[symbols][i+1] and nethold == 1000:
				share.append(-2000)
				date.append(df.index[i])
				nethold += -2000
		if nethold != 0:
			share.append(-nethold)
			date.append(df.index[len(df.index)-1])
			
		df_trades = pd.DataFrame(data = share, index = date, columns = ['orders'])
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
		df_bchm = pd.DataFrame(data = share, index = date, columns = ['orders'])
		#print df_bchm
		return df_bchm

def main():

	start_date = '2008-1-1'
	end_date = '2009-12-31'
	symbols = 'JPM'
    
	bps = BestPossibleStrategy()
	df_trades = bps.testPolicy(symbols, start_date, end_date, 100000)
	port_vals = compute_portvals(orders = df_trades, start_val = 100000, commission=0.00, impact=0.00)
	df_bchm = bps.benchMark(symbols, start_date, end_date, 100000)
	port_vals_bchm = compute_portvals(orders = df_bchm, start_val = 100000, commission=0.00, impact=0.00)
	#print port_vals, port_vals_bchm

	cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(port_vals)
	cum_ret_bchm, avg_daily_ret_bchm, std_daily_ret_bchm, sharpe_ratio_bchm = compute_portfolio_stats(port_vals_bchm)

	# Compare portfolio against $SPX
	print "Date Range: {} to {}".format(start_date, end_date)
	print
	print "Cumulative Return of Portfolio: {}".format(cum_ret)
	print "Cumulative Return of Benchmark: {}".format(cum_ret_bchm)
	print
	print "Standard Deviation of Portfolio: {}".format(std_daily_ret)
	print "Standard Deviation of Benchmark: {}".format(std_daily_ret_bchm)
	print
	print "Average Daily Return of Portfolio: {}".format(avg_daily_ret)
	print "Average Daily Return of Benchmark: {}".format(avg_daily_ret_bchm)
	print
	print "Sharpe Ratio of Portfolio: {}".format(sharpe_ratio)
	print "Sharpe Ratio of Benchmark: {}".format(sharpe_ratio_bchm)	
	print
	print "Final Portfolio Value: {}".format(port_vals[-1])
	print "Final Benchmark Value: {}".format(port_vals_bchm[-1])
	
	port_vals_bchm_norm = port_vals_bchm / port_vals_bchm.ix[0,]
	port_vals_norm = port_vals / port_vals.ix[0,]
	port_vals_bchm_norm = port_vals_bchm_norm.to_frame()
	port_vals_norm = port_vals_norm.to_frame()

	f1 = plt.figure(1)
	re = port_vals_bchm_norm.join(port_vals_norm, lsuffix = '_benchmark', rsuffix = '_portfolio')
	re.columns = ['Benchmark','Value of the best possible portfolio']
	ax = re.plot(title="Normalized Benchmark and Value of The Best Possible Portfolio", fontsize=12, color = ["blue","black"])
	ax.set_xlabel("Date")
	ax.set_ylabel("Portfolio")
	f1.show()	
	plt.show()

if __name__ == "__main__":
    main()
				
