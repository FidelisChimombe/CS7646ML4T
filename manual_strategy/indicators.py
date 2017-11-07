import pandas as pd
import numpy as np
import datetime as dt
import os
import matplotlib.pyplot as plt
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

def main():
    # Define input parameters
    start_date = '2008-1-1'
    end_date = '2009-12-31'
    dates = pd.date_range(start_date,end_date)
    symbols = 'JPM'
    window = 20
    
    df_init = get_data([symbols],dates,False)
    df_fill = df_init.fillna(method='ffill')
    df_fill = df_init.fillna(method='bfill')
    df = df_fill / df_fill.ix[0,] 
    #print df
    rm = get_rolling_mean(df[symbols],window)
    rstd = get_rolling_std(df[symbols],window)
    upper_band, lower_band = get_bollinger_bands(rm,rstd)

    SMA = get_rolling_mean(df[symbols],window)
    div = df.divide(SMA, axis='index')
    #print div
    BB = get_bollinger_value(df[symbols],window)
    #print SMA,BB
    Momentum = get_momentum_value(df[symbols],window)

    f1 = plt.figure(1)
    re = df.join(SMA, lsuffix = '_Normalized Price', rsuffix = '_SMA').join(div, lsuffix = '', rsuffix = '_NormPrice/SMA')
    re.columns = ['Normalized Price','SMA','Normalized Price/SMA']
    ax = re.plot(title="Normalized Price & SMA", fontsize=12, lw=1)
    ax.set_xlabel("Date")
    #ax.set_ylabel("Normalized Price")
    f1.show()

    f2 = plt.figure(2)
    re = df.join(SMA, lsuffix = '_Normalized Price', rsuffix = '_SMA').join(upper_band, lsuffix = '_', rsuffix = '_upperband').join(lower_band, lsuffix = '_', rsuffix = '_lowerband')
    re.columns = ['Normalized Price','SMA','Upper Bands', 'Lower Bands']
    ax = re.plot(title="Normalized Price & Bollinger bands", fontsize=12, lw=1)
    ax.set_xlabel("Date")
    #ax.set_ylabel("Normalized Price")
    f2.show()
 
    f3 = plt.figure(3)
    re = df.join(Momentum, lsuffix = '_Normalized Price', rsuffix = '_Momentum')
    re.columns = ['Normalized Price', 'Momentum']
    ax = re.plot(title="Normalized Price & Momentum", fontsize=12, lw=1)
    ax.set_xlabel("Date")
    #ax.set_ylabel("Normalized Price")
    f3.show()
    
    plt.show()

if __name__ == "__main__":
    main()
