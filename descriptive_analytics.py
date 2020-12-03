# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 18:50:32 2020

@author: JDela
"""
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import datetime as dt
import yfinance as yf



def get_csv_data():
    print('\nPlease make sure that you have exported the desired historical data as a csv file (Option 3 from the main menu).\n')   
    csv_data = None
    while csv_data is None:
        try:
            symbol = input("Please enter a valid the ticker symbol: ")
            start = input("""
Please enter time ranges in the format (YYYY-MM-DD). Example: 2019-12-31
Please enter a starting date: """)
            end = input("""
Please enter time ranges in the format (YYYY-MM-DD). Example: 2019-12-31
Please enter an ending date: """)
            interval = input("""
Example time ranges: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
Please enter a valid interval: """)
            price = input("""
Please pick your pricing measure (Open, High, Low, Close)
Please enter a valid price: """)            
            csv_data = symbol
        except FileNotFoundError:
            print('Invalid file or path.\n Please try again') 
            
#This retrieves the company name from Yahoo Finance despite the dataframe coming from a downloaded csv file
    company = yf.Ticker(symbol).info['longName']
        
    stock_df = pd.read_csv(symbol + ".csv")
    
    return symbol, start, end, interval, price, company, stock_df


#Code was adapted from MIS41110 lectures and tutorials
def raw_time_series():
    symbol, start, end, interval, price, company, stock_df = get_csv_data()
    #Close = stock_df.Close
    #Date = stock_df.Date
    
    print(type(stock_df))
    print(stock_df)
    
    plot = stock_df.plot(x='Date', y=price)

    
    plot.set_xlabel("Date")
    plot.set_ylabel('Price at ' + price)
    plot.set_title('Raw time series for ' + company)
    plot.ticklabel_format(axis = 'y', style = 'plain')

    plt.show()


def linear_regression():
    symbol, start, end, interval, price, company, stock_df = get_csv_data()
    
    #attempted to use this to convert the x-axis to actual dates but couldn't find a solution
    strDates = []
    strDates = stock_df['Date']
    
    #converts string dates to ordinal values to be able to perform the operation below
    stock_df['Date'] = pd.to_datetime(stock_df['Date'])
    stock_df['Date']= stock_df['Date'].map(dt.datetime.toordinal)
    
    #adapted from lecture material
    lr = stats.linregress(stock_df.Date, stock_df.Close)
    x = stock_df.Date
    y = lr.intercept + lr.slope * x
    stock_df.plot(x = "Date", y ="Close",linewidth=3, figsize=(12,6))
    
    #plots a linear trend line using a simple regression formula
    plt.plot(x, y, 'r') # ’r’ = red

  
    # modify ticks size
    plt.legend(labels =['Closing Price', 'Linear Trend Line'], fontsize=14)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    
    #Titles and labels for graph
    plt.title('Linear trend line for ' + company, fontsize=20)
    plt.xlabel('Days in Ordinal Form', fontsize=16)
    plt.ylabel('Closing Price', fontsize=16)
        
    plt.show()


#Code was adapted from https://towardsdatascience.com/moving-averages-in-python-16170e20f6c
def simple_moving_average():
    symbol, start, end, interval, price, company, stock_df = get_csv_data()
    stock_df.set_index('Date', inplace=True)

    #stock_df['Close'] = stock_df.mean(axis=1)
    stock_df = stock_df[['Close']]
    
    stock_df['SMA_50'] = stock_df.Close.rolling(50, min_periods=1).mean()
    stock_df['SMA_200'] = stock_df.Close.rolling(200, min_periods=1).mean()
    
    print(stock_df)
    
    # colors for the line plot
    colors = ['green', 'red', 'purple']
    
    # line plot 
    stock_df.plot(color=colors, linewidth=3, figsize=(12,6))
    
    # modify ticks size
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(labels =['Closing Price', '50-day SMA', '200-day SMA'], fontsize=14)
    
    # title and labels
    plt.title('Simple moving average for ' + company, fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Closing Price', fontsize=16)
    plt.show()


#Code was adapted from https://towardsdatascience.com/moving-averages-in-python-16170e20f6c
def cumulative_moving_average():
    symbol, start, end, interval, price, company, stock_df = get_csv_data()
    stock_df.set_index('Date', inplace=True)

    #stock_df['Close'] = stock_df.mean(axis=1)
    stock_df = stock_df[['Close']]   
    
    stock_df['CMA'] = stock_df.Close.expanding().mean()
    # colors for the line plot
    colors = ['green', 'orange']
    
    # line plot
    stock_df[['Close', 'CMA']].plot(color=colors, linewidth=3, figsize=(12,6))
    
    # modify ticks size
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(labels =['Closing Price', 'CMA'], fontsize=14)
    
    # title and labels
    plt.title('Cumulative moving average for ' + company, fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Closing Price', fontsize=16)
    plt.show()

#Code was adapted from https://towardsdatascience.com/moving-averages-in-python-16170e20f6c
def exponential_moving_average():
    symbol, start, end, interval, price, company, stock_df = get_csv_data()
    stock_df.set_index('Date', inplace=True)

    #stock_df['Close'] = stock_df.mean(axis=1)
    stock_df = stock_df[['Close']]   
    
    # cumulative moving average
    stock_df['EMA_0.1'] = stock_df.Close.ewm(alpha=0.1, adjust=False).mean()
    
    # smoothing factor - 0.3
    stock_df['EMA_0.3'] = stock_df.Close.ewm(alpha=0.3, adjust=False).mean() 
    
    
    # colors for the line plot
    colors = ['green', 'orchid', 'orange']
    
    # line plot 
    stock_df[['Close', 'EMA_0.1', 'EMA_0.3']].plot(color=colors, linewidth=3, figsize=(12,6), alpha=0.8)
    
    # modify ticks size
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(labels=['Closing Price', 'EMA - alpha=0.1', 'EMA - alpha=0.3'], fontsize=14)
    
    # title and labels
    plt.title('The exponential moving average for ' + company, fontsize=20)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Closing Price', fontsize=16)
    plt.show()
    
    
# Code was adapted from the following tutorial https://towardsdatascience.com/implementing-macd-in-python-cc9b2280126a    
def moving_average_convergence_divergence():
    symbol, start, end, interval, price, company, stock_df = get_csv_data()   
    
    exp1 = stock_df.Close.ewm(span=12, adjust=False).mean()
    exp2 = stock_df.Close.ewm(span=26, adjust=False).mean()
    exp3 = stock_df.Close.ewm(span=9, adjust=False).mean()
    macd = exp1-exp2
    plt.plot(stock_df.Date, stock_df.Close, label= symbol.upper() + 'Closing Price')
    plt.plot(stock_df.Date, macd, label='MACD', color='orange')
    plt.plot(stock_df.Date, exp3, label=' Signal Line', color='Magenta')
    plt.legend(loc='upper left')
    
    # title and labels
    plt.title('The moving average convergence / divergence ' + company)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Closing Price', fontsize=16)
    
    plt.show()