"""
Name: Yangfan Zhang
User ID: yzhang3067
"""
import pandas as pd
import numpy as np
import datetime as dt
import os
import sys
import matplotlib.pyplot as plt
from util import get_data, plot_data
import ManualStrategy as ms
import StrategyLearner as sl
from marketsimcode import compute_portvals

def compute_portfolio_stats(daily_port):
	daily_rets = ( daily_port / daily_port.shift(1)) - 1
	cr = (daily_port.iloc[-1,0] / daily_port.iloc[0,0]) - 1
	adr = daily_rets.mean()
	sddr = daily_rets.std()
	sr = np.sqrt(252.0) * ((daily_rets - 0.0).mean() / sddr)
	return cr, adr, sddr, sr

def main():

	#display function for in sample data	
	sd = dt.datetime(2008,1,1)
	ed = dt.datetime(2009,12,31)
	symbol = 'JPM'
	sv = 100000;


	manual = ms.ManualStrategy()
	strategy = sl.StrategyLearner(verbose = False, impact=0.005)
	strategy.addEvidence(symbol, sd, ed, sv)
	df_trades = strategy.testPolicy(symbol, sd, ed, sv)
	print df_trades
	table = manual.testPolicy(symbol, sd ,ed, sv)
	print table
	df_bchm = manual.benchMark(symbol, sd, ed, sv)
	print df_bchm

	port_vals, port_vals_bchm, signal = compute_portvals(df_trades, sv, 0.00, 0.005)
	print port_vals, port_vals_bchm
	manu_vals, port_vals_bchm, signal = compute_portvals(table, sv, 0.00, 0.005)
	#port_vals_bchm, port_vals_bchm,signal = compute_portvals(orders = df_bchm, start_val = 100000, commission=0.00, impact=0.00)

	port_vals = port_vals / port_vals.ix[0,]
	manu_vals = manu_vals / manu_vals.ix[0,]	
	port_vals_bchm = port_vals_bchm / port_vals_bchm.ix[0,]
	#df_bchm = manual.benchMark(symbols, start_date, end_date, 100000)
	#port_vals_bchm = compute_portvals(orders = df_bchm, start_val = 100000, commission=0.00, impact=0.00)
	print port_vals, manu_vals, port_vals_bchm
	#port_vals = port_vals.Value
	cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = compute_portfolio_stats(port_vals)
	cum_ret_manu, avg_daily_ret_manu, std_daily_ret_manu, sharpe_ratio_manu = compute_portfolio_stats(manu_vals)
	cum_ret_bchm, avg_daily_ret_bchm, std_daily_ret_bchm, sharpe_ratio_bchm = compute_portfolio_stats(port_vals_bchm)

	# Compare portfolio against $SPX
	print "Date Range(In Sample): {} to {}".format(sd, ed)
	print
	print "In Sample Cumulative Return of Machine Learning Strategy: {}".format(cum_ret)
	print "In Sample Cumulative Return of Manual Strategy: {}".format(cum_ret_manu)	
	print "In Sample Cumulative Return of Benchmark: {}".format(cum_ret_bchm)
	print
	print "In Sample Standard Deviation of Machine Learning Strategy: {}".format(std_daily_ret)
	print "In Sample Standard Deviation of Manual Strategy: {}".format(avg_daily_ret_manu)
	print "In Sample Standard Deviation of Benchmark: {}".format(std_daily_ret_bchm)
	print
	print "In Sample Average Daily Return of Machine Learning Strategy: {}".format(avg_daily_ret)
	print "In Sample Average Daily Return of Manual Strategy: {}".format(std_daily_ret_manu)
	print "In Sample Average Daily Return of Benchmark: {}".format(avg_daily_ret_bchm)
	print
	print "In Sample Sharpe Ratio of Machine Learning Strategy: {}".format(sharpe_ratio)
	print "In Sample Sharpe Ratio of Manual Strategy: {}".format(sharpe_ratio_manu)
	print "In Sample Sharpe Ratio of Benchmark: {}".format(sharpe_ratio_bchm)	
	print
	print "In Sample Final Portfolio Value of Machine Learning Strategy: {}".format(port_vals.ix[-1,0]*sv)
	print "In Sample Final Portfolio Value of Manual Strategy: {}".format(manu_vals.ix[-1,0]*sv)
	print "In Sample Final Portfolio Value of Benchmark: {}".format(port_vals_bchm.ix[-1,0]*sv)

	f1 = plt.figure(1)
	re = port_vals_bchm.join(manu_vals, lsuffix = '_benchmark', rsuffix = '_manual').join(port_vals, lsuffix = '_lala', rsuffix = '_portfolio')
	re.columns = ['Portfolio of Benchmark','Portfolio of the Manual Strategy','Portfolio of the Machine Learning Strategy']
	ax = re.plot(title="Normalized Portfolio of Benchmark, Manual Strategy, Machine Learning Strategy", fontsize=12, color = ["black","green","red"])
	ax.set_xlabel("Date")
	ax.set_ylabel("Portfolio")
	f1.show()
	plt.show()

if __name__ == "__main__":
	main()
