# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 00:22:46 2020

@author: JDela

PROJECT SCOPE

Search for specific stocks, and query specified time ranges, along with associated analysis, 
such as statistical descriptions of prices and/or volume (mean, median, range, etc), 
technical indicators, visualisation (of the raw data, but also of transformations, such as 
moving averages), and even basic modelling (such as regression).

Provide a comprehensive but easy to use and intuitive interface (text or graphical).

Descriptive Analytics:
1. Mean;
2. Quartiles;
3. Range (max-min);
4. Standard variation;
5. Co-efficient of variation;
6. price values; etc.


Predictive Analytics:
1. The user specifies the modelling period (i.e. the training data);
2. They also specify a date for which they require a prediction;
3. A linear model is built, using the specified period;
4. The prediction is produced, along with the model’s RMSE and R2 value (co-efficient of determination).

"""
#Declaring all imported packages at the top of the page
#import numpy as np
import pandas as pd
from yahoo_finance import get_ticker_data, download_ticker_data

#Basic welcome message
def display_welcome():
    print('Welcome to the Cobra Stock Analysis Application')

#Providing a text based interface to begin with
def display_interface():
    print('Use the options below to navigate the application:')
    print("""
          0. Quit
          1. Search NASDAQ Stocks (Offline)
          2. Search Real-time Historical Data (Yahoo Finance)
          3. Export Historical Data (Yahoo Finance)
          4. Something
          5. Help
          """) #Options enable user to navigate

#Retrieves the contents of help.txt and displays it for the user
def display_help():
    for line in open("help.txt"):
        print(line, end = "")
        
#Pandas reads the Excel csv company list file and returns the contents in an array        
def import_company_list():
    return pd.read_csv('companylist.csv')

#Returns the users selected option
def interface_selection():
    return input("Please choose option: ")
    #print("\n")

#Returns the stocks or companies that the user specifies with their input
def search_stocks(company_list):
    print('Search for stocks from localised NASDAQ data')
    symbol = input("Please choose ticker symbol: ")
    search_results = company_list[(company_list.Symbol.str.lower().str.contains(symbol.lower())) 
               | (company_list.Name.str.lower().str.contains(symbol.lower()))]
    print(search_results)
    #print(search_results.describe())
    return search_results

#This calls the 'yahoo_finance' module and returns the data for the specified ticker symbol
def retrieve_historical_data():
    print('View historical stock data for a specified time range')
    print('Example time ranges: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max')   
    
#This passes the input values into the 'yahoo_finance' module    
    data =  None
    while data is None:    
        try:
            symbol = input("Please choose ticker symbol: ")
            period = input("Please choose time period: ")
            data = get_ticker_data(symbol, period)
        except KeyError: 
            print('Invalid ticker symbol or time period.\n Please try again.')

#This calls the 'yahoo_finance' module and export the data for the specified ticker symbol in a csv file
def export_historical_data():
    print('Export historical stock data for a specified time range')
    print('Please enter time ranges in the format (YYYY-MM-DD). Example: 2019-12-31 ')   
    
#This passes the input values into the 'yahoo_finance' module    
    data =  None
    while data is None:    
        try:
            symbol = input("Please choose ticker symbol: ")
            start = input("Please choose start period: ")
            end = input("Please choose end period: ")
            data = download_ticker_data(symbol, start, end)
        except KeyError: 
            print('Invalid ticker symbol or time range.\n Please try again.')        

#Performs the relevant operation based on the users selection
def process_selection(option, company_list):
    while option != "0":
        if option == "1": # Searches stocks
            search_stocks(company_list)
            print("\n")
        elif option == "2": # Gets historical data from yfinance
            retrieve_historical_data()
            print("\n")
        elif option == "3": # Exports the stock data into a csv file
            export_historical_data()
            print("\n")                  
        elif option == "4": # Add feature
            print('Add feature')
            print("\n")            
        elif option == "5": # Help provided
            display_help()
            print("\n")
        else:  # Wrong choice
            print("Invalid input, please try again.")
            print("\n")
            
        #Redisplay the user options
        display_interface()
        option = interface_selection()

#Calls the relevant functions to run the application
def main():
  
    company_list = import_company_list()
    
    display_welcome()
    
    display_interface()
    
    option = interface_selection()
    
    
    process_selection(option, company_list)
    
if __name__ == '__main__':
    main()

