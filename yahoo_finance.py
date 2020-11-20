# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:40:05 2020

@author: JDela
"""

import yfinance as yf
import matplotlib.pyplot as plt
import seaborn

from matplotlib.backends.backend_pdf import PdfPages

#Code for yfinance was provided in a tutorial and is available from 
#https://towardsdatascience.com/free-stock-data-for-python-using-yahoo-finance-api-9dafd96cad2e

def get_ticker_data(symbol, period):
    #Retrieves the stock specified from the ticker 
    msft = yf.Ticker(symbol)
    
    # get stock info
    print(msft.info)
    
    # get historical market data
    hist = msft.history(period=period)
    
    print(type(hist))
    print(hist)
    
    hist['Close'].plot(figsize=(16,9))
    plt.show()
    return hist

#get_ticker_data(symbol, period)

def download_ticker_data(symbol, start, end):
# Download stock data then export as CSV
    data_df = yf.download(symbol, start=start, end=end)
    data_df.to_csv(symbol.lower() + '.csv')
    return data_df


#Plots the stock and exports it to a pdf
# =============================================================================
# with PdfPages(r'charts.pdf') as export_pdf:
#     hist['Close'].plot(figsize=(16,9))
#     export_pdf.savefig()
# =============================================================================
