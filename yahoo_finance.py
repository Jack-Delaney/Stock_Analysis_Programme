# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:40:05 2020

@author: JDela
"""

import yfinance as yf
import matplotlib.pyplot as plt
import seaborn
import datetime as dt


from matplotlib.backends.backend_pdf import PdfPages

#Code for yfinance was provided in a tutorial and is available from 
#https://towardsdatascience.com/free-stock-data-for-python-using-yahoo-finance-api-9dafd96cad2e

def get_ticker_data(symbol, period):
    
    #Retrieves the stock specified from the ticker 
    stock = yf.Ticker(symbol)
    
    # get stock info
    #print(stock.info)
    
    # get historical market data
    historical_data = stock.history(period=period)
    print('\nSector: ' + stock.info['sector'])
    print('\nDaily Trading Volume (10 Day Average): ' + str(stock.info['averageDailyVolume10Day']))
    print('\nHighest / Lowest Value (Last 52 Weeks): ' + str(stock.info['fiftyTwoWeekHigh']) + ' / ' + str(stock.info['fiftyTwoWeekLow']))    
   
    # prints the stock data and basic pandas description 
    print('\nHistorical stock data for ' + stock.info['longName'] )
    print(historical_data)
    print('\nBasic descriptive analytics for ' +stock.info['longName'])
    print(historical_data.describe())
    
    #historical_data['Close'].plot(figsize=(16,9))

    
    #plt.show()
    
    
    return historical_data

#get_ticker_data(symbol, period)

def download_ticker_data(symbol, start, end):
# Download stock data then export as CSV
    stock_df = yf.download(symbol, start=start, end=end)
    stock_df.to_csv(symbol.lower() + '.csv')
    return stock_df


#Plots the stock and exports it to a pdf
# =============================================================================
# with PdfPages(r'charts.pdf') as export_pdf:
#     hist['Close'].plot(figsize=(16,9))
#     export_pdf.savefig()
# =============================================================================
