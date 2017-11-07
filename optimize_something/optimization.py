"""MC1-P2: Optimize a portfolio."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from util import get_data, plot_data
import scipy.optimize as spo

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def compute_portfolio(allocs, prices, sv = 1):
    normed = prices / prices.ix[0,]
    alloced = normed * allocs
    pos_vals = alloced * sv
    port_val = pos_vals.sum(axis = 1)
    return port_val

def compute_portfolio_stats(allocs, prices, rfr = 0.0, sf = 252.0):
    port_val = compute_portfolio(allocs, prices, 1)
    daily_ret = port_val.copy()
    daily_ret = (daily_ret/daily_ret.shift(1)) - 1   
    cr = (port_val[-1]/port_val[0]) - 1
    adr = daily_ret.mean()
    sddr = daily_ret.std()
    sr = np.sqrt(sf) * ((daily_ret - rfr).mean() / sddr)
    return cr,adr,sddr,sr

def optimize_helper(allocs, prices):
    port_val = compute_portfolio(allocs, prices, 1)
    cr, adr, sddr, sr = compute_portfolio_stats(allocs, prices, 0.0, 252.0)
    return sddr

def optimize_allocations(prices):
    alloc = 1.0/prices.shape[1]
    allocs = [alloc] * prices.shape[1]
    bnds = [(0.0,1.0),] * prices.shape[1]
    result = spo.minimize(optimize_helper, allocs, args = (prices,), method = 'SLSQP', options = {'disp':False},  bounds = bnds, constraints = ({'type': 'eq', 'fun': lambda x: 1.0 - sum(x)}))
    allocs = result.x
    return allocs

def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    # note that the values here ARE NOT meant to be correct for a test case
    allocs = np.asarray([0.2, 0.2, 0.3, 0.3]) # add code here to find the allocations
    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1] # add code here to compute stats
    allocs = optimize_allocations(prices)
    # Get daily portfolio value
    port_val = prices_SPY # add code here to compute daily portfolio values
    port_val = compute_portfolio(allocs, prices, 1)
    cr, adr, sddr, sr = compute_portfolio_stats(allocs, prices, 0.0, 252.0)
    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=['Portfolio', 'SPY'], axis=1)
        #pass
        df_temp = df_temp / df_temp.ix[0]
        ax = df_temp.plot(title = "Daily Portfolio Value and SPY")
        ax.set_ylabel("Normalized price")
        ax.set_xlabel("Date")
        ax.grid(True, 'both')
        plt.show()
    return allocs, cr, adr, sddr, sr

def test_code():
    # This function WILL NOT be called by the auto grader
    # Do not assume that any variables defined here are available to your function/code
    # It is only here to help you set up and test your code

    # Define input parameters
    # Note that ALL of these values will be set to different values by
    # the autograder!

    # start_date = dt.datetime(2009,1,1)
    # end_date = dt.datetime(2010,1,1)
    # symbols = ['GOOG', 'AAPL', 'GLD', 'XOM', 'IBM']
    
    start_date = dt.datetime(2008,6,1)
    end_date = dt.datetime(2009,6,1)
    symbols = ['IBM','X','GLD']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = False)

    # Print statistics
    print "Start Date:", start_date
    print "End Date:", end_date
    print "Symbols:", symbols
    print "Allocations:", allocations
    print "Sharpe Ratio:", sr
    print "Volatility (stdev of daily returns):", sddr
    print "Average Daily Return:", adr
    print "Cumulative Return:", cr

if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
