"""
Name: Yangfan Zhang
User ID: yzhang3067
"""
import pandas as pd
import numpy as np
import datetime as dt
import os
from util import get_data, plot_data

def Bollinger(sd = dt.datetime(2010,1,1), ed = dt.datetime(2011,12,31), 
	syms = ['JPM'],gen_plot=True):
	
    # read data
    dates = pd.date_range(sd, ed)
    symbol = syms
    price = get_data(symbol, dates)
    price = price[symbol]   
    price = price / price.ix[0,] 
	
    std = pd.rolling_std(price[symbol], window = 20)
    df = pd.rolling_mean(price[symbol], window = 20)
    upper = df + std * 2
    lower = df - std * 2
    upper_one = df + std
    lower_one = df - std  
 
    if gen_plot:
    	ax = df.plot(title = "Bollinger Band",label='SMA')
    	upper.plot(label='Upper Band', ax = ax)
    	lower.plot(label='Lower Band', ax = ax)
    	price.plot(label='JPM Price',ax = ax) 
	ax.legend(["SMA", "Upper Band","Lower Band","JPM Price"]);   
    	ax.set_xlabel("Date")
    	ax.set_ylabel("Price")
    	ax.legend(loc='lower right')
    	plt.show()
    
    return df, upper, lower, upper_one, lower_one

def Momentum(sd = dt.datetime(2010,1,1), ed = dt.datetime(2011,12,31),
        syms = ['JPM'],gen_plot=True):
    
    dates = pd.date_range(sd, ed)
    symbol = syms
    price = get_data(symbol, dates)
    price = price[symbol]
    price = price / price.ix[0,]

    momentum = price / price.shift(periods = 10) - 1

    if gen_plot:
        ax = price.plot(title = "Momentum", label='JPM Price')
        momentum.columns = ['Momentum']
        momentum.plot(label = 'Momentum', ax = ax)
	ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend(loc='lower right')
        plt.show()

    momentum = pd.DataFrame(data=momentum.ix[:,0])
    return momentum

def SMA(sd = dt.datetime(2010,1,1), ed = dt.datetime(2011,12,31),
        syms = ['JPM'],gen_plot=True):

    dates = pd.date_range(sd, ed)
    symbol = syms
    price = get_data(symbol, dates)
    price = price[symbol]
    price = price / price.ix[0,]

    sma = pd.rolling_mean(price[symbol], window = 20)   
    quo = price.divide(sma, axis='index')
    quo.columns = ['Price/SMA']	     
    sma = sma.iloc[20:]    

    if gen_plot:
        ax = sma.plot(title = "SMA", label='SMA')
        quo.plot(label = 'JPM Price/SMA', ax = ax)
        #quo.columns = ['Price/SMA']
 	price.plot(label = 'Price', ax = ax)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend(loc='lower right')
        plt.show()

    return sma,quo

def STD(sd = dt.datetime(2010,1,1), ed = dt.datetime(2011,12,31),
        syms = ['JPM'],gen_plot=True):
    dates = pd.date_range(sd, ed)
    symbol = syms
    price = get_data(symbol, dates)
    price = price[symbol]
    price = price / price.ix[0,]
    std = pd.rolling_std(price[symbol], window = 20)
    if gen_plot:
        ax = std.plot(title = "Standard Deviation", label='STD')
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend(loc='lower right')
        plt.show()
    return std