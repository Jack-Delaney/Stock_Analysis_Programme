# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Sun Nov 29 18:50:32 2020

@author: JDela
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from scipy import stats
import datetime as dt
import yfinance as yf
from pylab import rcParams
import statsmodels.api as sm



#This function gets input from the user and returns data from the appropriate csv file
def get_csv_data():
    print('\nPlease make sure that you have exported the desired historical data as a csv file (Option 3 from the main menu).\n')   
    csv_data = None
    while csv_data is None:
        try:
            symbol = input("Please enter a valid the ticker symbol: ").lower()
#             start = input("""
# Please enter time ranges in the format (YYYY-MM-DD). Example: 2019-12-31
# Please enter a starting date: """)
#             end = input("""
# Please enter time ranges in the format (YYYY-MM-DD). Example: 2019-12-31
# Please enter an ending date: """)
#             interval = input("""
# Example time ranges: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
# Please enter a valid interval: """)
#             price = input("""
# Please pick your pricing measure (Open, High, Low, Close)
# Please enter a valid price: """)            
            csv_data = symbol
        except FileNotFoundError:
            print('Invalid file or path.\n Please try again') 
            
#This retrieves the company name from Yahoo Finance despite the dataframe coming from a downloaded csv file
    company = yf.Ticker(symbol).info['longName']
      
    #Returns a pandas dataframe from the specified csv file
    stock_df = pd.read_csv(symbol + ".csv")
    
    return symbol, company, stock_df


#Code was adapted from MIS41110 lectures and tutorials
def raw_time_series():
    """
    This just returns basic graphs of the stock prices over time, without any meaningful calculations
    """
    symbol, company, stock_df = get_csv_data()
    price = input("""
    Please pick your pricing measure (Open, High, Low, Close)
    Please enter a valid price: """)   
    #Close = stock_df.Close
    #Date = stock_df.Date
    
    # print(type(stock_df))
    # print(stock_df)
    
    #plots the user specified price measure against date
    plot = stock_df.plot(x='Date', y=price)

    #renaming the details of the graph
    plot.set_xlabel("Date")
    plot.set_ylabel('Price at ' + price)
    plot.set_title('Raw time series for ' + company)
    plot.ticklabel_format(axis = 'y', style = 'plain')
    plt.show()

    #code for following graphs was adapted from https://towardsdatascience.com/an-end-to-end-project-on-time-series-analysis-and-forecasting-with-python-4835e6bf050b
    matplotlib.rcParams['axes.labelsize'] = 14
    matplotlib.rcParams['xtick.labelsize'] = 12
    matplotlib.rcParams['ytick.labelsize'] = 12
    matplotlib.rcParams['text.color'] = 'k'
 
    #Converting Date to datetime so that it works for the operations below
    stock_df['Date'] = pd.to_datetime(stock_df.Date)
    #stock_df.index = stock_df['Date']   
    
    #Removes the other columns from the dataframe
    data = stock_df.filter(['Date',price])

    #setting the data as the index so that it can be plotted against 'price'
    data = data.set_index('Date')
    
    #returns the monthly average 'price'
    y = data[price].resample('MS').mean()
    
    #renaming details of the graph
    plot2 = y.plot(figsize=(15, 6))
    plot2.set_xlabel("Date")
    plot2.set_ylabel('Price at ' + price)
    plot2.set_title('Average monthly ' + price + ' price for ' + company)
    plt.show()
    
    #decomposition graphs from the link above
    rcParams['figure.figsize'] = 18, 8
    decomposition = sm.tsa.seasonal_decompose(y, model='additive')
    fig = decomposition.plot()
    #fig.set_title('Time series decompisition for ' + company)
    plt.show()


#Code adapted from the pandas lecture
def trend_line():
    symbol, company, stock_df = get_csv_data()
    
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
    symbol, company, stock_df = get_csv_data()
    
    #setting date as index for dataframe
    stock_df.set_index('Date', inplace=True)

    #stock_df['Close'] = stock_df.mean(axis=1)
    stock_df = stock_df[['Close']]
    
    #converts the simple moving average for a specified number of days
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
    symbol, company, stock_df = get_csv_data()
    
    #Sets date as index for the dataframe
    stock_df.set_index('Date', inplace=True)

    #stock_df['Close'] = stock_df.mean(axis=1)
    
    #removes the other columns from the dataframe
    stock_df = stock_df[['Close']]   
    
    #calculations for cumulative moving average
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
    symbol, company, stock_df = get_csv_data()
   
    #making date the index for the dataframe
    stock_df.set_index('Date', inplace=True)

    #stock_df['Close'] = stock_df.mean(axis=1)
    
    #returns just the close column
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
    symbol, company, stock_df = get_csv_data()   
    
    print('Processing may take up to a minute')
    
    #performs the calculations for macd
    exp1 = stock_df.Close.ewm(span=12, adjust=False).mean()
    exp2 = stock_df.Close.ewm(span=26, adjust=False).mean()
    exp3 = stock_df.Close.ewm(span=9, adjust=False).mean()
    macd = exp1-exp2
    plt.plot(stock_df.Date, stock_df.Close, label= symbol.upper() + 'Closing Price')
    plt.plot(stock_df.Date, macd, label='MACD', color='orange')
    plt.plot(stock_df.Date, exp3, label=' Signal Line', color='Magenta')
    plt.legend(loc='upper left')
    print('The moving average convergence divergence for ' + company + ' is ' + str(macd))
    
    
    # title and labels
    plt.title('The moving average convergence / divergence ' + company)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Closing Price', fontsize=16) 
    plt.show()