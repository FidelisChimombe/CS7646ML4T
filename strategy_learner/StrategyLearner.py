"""
Name: Yangfan Zhang
User ID: yzhang3067
"""

import datetime as dt
import pandas as pd
import util as ut
import random
from indicators import SMA, Momentum, Bollinger, STD
import BagLearner as bl
import numpy as np

class StrategyLearner(object):

	# constructor
	def __init__(self, verbose = False, impact=0.0):
		self.verbose = verbose
		self.impact = impact
		self.N = 10 # N for N days return
		self.learner = bl.BagLearner(kwargs = {"leaf_size":5,"verbose":False},bags = 20)

	# this method should create a QLearner, and train it for trading
	def addEvidence(self, symbol = "IBM", \
		sd=dt.datetime(2008,1,1), \
		ed=dt.datetime(2009,1,1), \
		sv = 10000): 

		# set parameters and get data for training
		syms = [symbol]
		dates = pd.date_range(sd, ed)
		prices_all = ut.get_data(syms, dates)  # automatically adds SPY
		prices = prices_all[syms]
		if self.verbose: print prices
		
		x_raw = self.getX_train(prices, sd, ed, syms)		
		x_train = x_raw[:,1:-1]

		y_raw = []
		for i in range(0, x_raw.shape[0]):
			if x_raw[i,-1] / x_raw[i,0] > 1.02+self.impact:
				y_raw.append(1)
			elif x_raw[i,-1] / x_raw[i,0] < 0.98-self.impact:
				y_raw.append(-1)
			else:
				y_raw.append(0)

		y_train = np.array(y_raw)

		# change to mode
		self.learner.addEvidence(x_train ,y_train)
		#print 'finished training'

	def getX_train(self, prices, sd, ed, syms):
		# add your code to do learning here
		# Calculate technical indicators and add to X value
		mean, upper, lower, upper_one, lower_one  = Bollinger(sd, ed, syms, False)
		momentum = Momentum(sd, ed, syms, False)
		sma,quo = SMA(sd, ed, syms, False)
		std = STD(sd, ed, syms, False)

		x_raw = np.zeros((len(prices) - self.N,9))
		# mismatch data of different data may cause learner get stupid
		for i in range(0, len(prices) - self.N):
			x_raw[i][0] = prices.iloc[i]
			x_raw[i][1] = prices.iloc[i] - upper_one.iloc[i]
			x_raw[i][2] = prices.iloc[i] - lower_one.iloc[i]
			x_raw[i][3] = momentum.iloc[i]
			x_raw[i][4] = quo.iloc[i]
			x_raw[i][5] = std.iloc[i]
			x_raw[i][6] = prices.iloc[i] - upper.iloc[i]
			x_raw[i][7] = prices.iloc[i] - lower.iloc[i]
			x_raw[i][8] = prices.iloc[i + self.N]
		    
		return x_raw

	def getX_test(self, prices, sd, ed, syms):
		# Calculate technical indicators and add to X value
		mean, upper, lower, upper_one, lower_one  = Bollinger(sd, ed, syms, False)
		momentum = Momentum(sd, ed, syms, False)
		sma,quo = SMA(sd, ed, syms, False)
		std = STD(sd, ed, syms, False)

		x_test = np.zeros((len(prices) - self.N,7))
		
		for i in range(0, len(prices) - self.N):
			x_test[i][0] = prices.iloc[i] - upper_one.iloc[i]
			x_test[i][1] = prices.iloc[i] - lower_one.iloc[i]
			x_test[i][2] = momentum.iloc[i]
			x_test[i][3] = quo.iloc[i]
			x_test[i][4] = std.iloc[i]
			x_test[i][5] = prices.iloc[i] - upper.iloc[i]
			x_test[i][6] = prices.iloc[i] - lower.iloc[i]

		return x_test
	# this method should use the existing policy and test it against new data
	def testPolicy(self, symbol = "IBM", \
		sd=dt.datetime(2009,1,1), \
		ed=dt.datetime(2010,1,1), \
		sv = 10000):

		# set parameters and get data for training
		syms = [symbol]
		dates = pd.date_range(sd, ed)
		prices_all = ut.get_data(syms, dates)  # automatically adds SPY
		prices = prices_all[syms]
		# get the trade table

		if self.verbose: print prices

		x_test = self.getX_test(prices, sd, ed, syms)
		y_query = self.learner.query(x_test)
		table = pd.DataFrame(0, columns=prices.columns, index=prices.index)

		share = 0
		for i in range(0, len(prices) - self.N):
			if y_query[i] == 1:
				if share == 0:
					share = 1000
					table.iloc[i, 0] = 1000
				elif share == - 1000:
					share = 1000
					table.iloc[i, 0] = 2000
			if y_query[i] == -1:
				if share == 0:
					share = -1000
					table.iloc[i, 0] = -1000
				elif share == 1000:
					share = -1000
					table.iloc[i, 0] = -2000
	
		return table

if __name__=="__main__":
    print "One does not simply think up a strategy"
