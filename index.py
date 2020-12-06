# -*- coding: utf-8 -*-
#!/usr/bin/env python
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
import numpy as np
import pandas as pd
import yfinance as yf
import datetime
from yahoo_finance import get_ticker_data, download_ticker_data
from descriptive_analytics import raw_time_series, trend_line, simple_moving_average, cumulative_moving_average, exponential_moving_average, moving_average_convergence_divergence
from predictive_analytics import linear_regression, lstm_prediction


#Basic welcome message
def display_welcome():
    print('Welcome to the Cobra Stock Analysis Application')


#Providing a text based interface for user initially
def display_main_menu():
    print('Use the options below to navigate the application:')
    print("""
          0. Quit
          1. Search NASDAQ Listed Companies (Offline)
          2. Search Real-time Historical Data With Basic Analytics And Profile (Yahoo Finance)
          3. Export Historical Data For Advanced Analytics (Yahoo Finance)
          4. Perform Advanced Descriptive Analytics (Offline)
          5. Perform Advanced Predictive Analytics (Offline)
          6. Help
          """) #Options enable user to navigate


#Providing a text based interface to access descriptive analytics
def display_descriptive_analytics():
    print('Use the options below to perform desired descriptive analytics:')
    print("""
          0. Back To Main Menu
          1. Raw Time-series
          2. Linear Trend Line
          3. Simple Moving Average
          4. Cumulative Moving Average
          5. Exponential Moving Average
          6. Moving Average Convergence/Divergence
          7. Help
          """) #Options enable user to navigate


#Providing a text based interface to access predictive analytics
def display_predictive_analytics():
    print('Use the options below to perform desired descriptive analytics:')
    print("""
          0. Back To Main Menu
          1. Linear Regression Prediction
          2. LSTM Prediction
          3. Help
          """) #Options enable user to navigate          
          
          
#Retrieves the contents of help.txt and displays it for the user
def display_help():
    for line in open("help.txt"):
        print(line, end = "")


#Pandas reads the Excel csv company list file and returns the contents in an array        
def import_company_list():
    return pd.read_csv('companylist.csv')


#Returns the value that the user enters in the text based interfaced
def get_user_selection():
    return input("Please choose option: ")
    #print("\n")


#Returns the stocks or companies that the user specifies with their input
def search_stocks(company_list):
    """
    The user can search the csv file downloaded from NASDAQ containing over 3000 companies. The search isn't
    resctricted to exact matches. The user can use this function to find out the ticker symbol for the desired
    company, assuming it is in the file. Otherwise they can try option 2, Yahoo Finance.
    """
    print('Search for stocks from localised NASDAQ data, provides ticker symbol for further options')
    symbol = input("Please enter company name or ticker symbol: ")
    
    #This enables the search results to include results that aren't exact matches but contain the specified words or letters
    #Though it does not show similar results or misspelled words
    search_results = company_list[(company_list.Symbol.str.lower().str.contains(symbol.lower())) 
               | (company_list.Name.str.lower().str.contains(symbol.lower()))]
    print(search_results)

    return search_results


#This calls the 'yahoo_finance' module and returns the data for the specified ticker symbol
def retrieve_historical_data():
    print('View historical stock data for a specified time range with basic descriptive analytics')
    print('Example time ranges: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max')   
    
#This passes the input values into the 'yahoo_finance' module    
    data =  None
    while data is None:    
        try:
            symbol = input("Please enter a valid ticker symbol: ")
            period = input("Please enter a valid time period: ")
            data = get_ticker_data(symbol, period)
        except KeyError: 
            print('Invalid ticker symbol or time period.\n Please try again.')

    
#Code adapted from https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python?fbclid=IwAR0amPCcLn54wJzJfSIfeALu4ZcSjD8BMyPSu0kgtEPrVF_LXqDt1-hX_5U
def validate(date_text):
    """
    This ensures that the input from the user must be of YYYY-MM-DD format, it raises a value error if it isn't
    which in turn can be handled in other functions.
    """    
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        #print(date_text)
    except ValueError:
        print('Error')
        raise ValueError('Invalid date input')        
        #export_historical_data()
        #raise ValueError("Incorrect data format, should be YYYY-MM-DD")


#This calls the 'yahoo_finance' module and export the data for the specified ticker symbol in a csv file
def export_historical_data():
    print('Export historical stock data for a specified time range')
    print('Please enter time ranges in the format (YYYY-MM-DD). Example: 2019-12-31 ')   
    
#This passes the input values into the 'yahoo_finance' module    
    data =  None
    while data is None:    
        try:
            symbol = input("Please enter a valid ticker symbol: ")
            
            # start = input("Please enter a valid start period: ")
            # end = input("Please enter a valid end period: ")
           
            #This uses the validate() function to ensure date formats are correct
            start_validation = None
            while start_validation is None:
                try:
                    start = input("Please enter a valid start period: ")
                    validate(start)
                    start_validation = start
                except ValueError:
                    print('Please make sure it is in the following format: YYYY-MM-DD')
                      
            #This uses the validate() function to ensure date formats are correct            
            end_validation = None
            while end_validation is None:
                try:
                    end = input("Please enter a valid end period: ")
                    validate(end)
                    end_validation = end
                except ValueError:
                    print('Please make sure it is in the following format: YYYY-MM-DD')

            #Calls the yahoo_finance module and exports the data to a csv file in the directory
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
        elif option == "4": # Performs descriptive analytics on a csv file
            descriptive_analytics()
            print("\n")   
        elif option == "5": # Performs Predictive analytics on a csv file
            predictive_analytics()
            print("\n")            
        elif option == "6": # Help provided via text from a csv file
            display_help()
            print("\n")
        else:  # Wrong choice
            print("Invalid input, please try again.")
            print("\n")
            
        # #Redisplay the user options
        display_main_menu()
        #gives the user's selected option a value
        option = get_user_selection()


#This returns the descriptive analytics menu and processes the choice using the function below
def descriptive_analytics():

    display_descriptive_analytics()
    descriptive_option = get_user_selection()
    process_descriptive_analytics(descriptive_option)


#Performs the relevant operation based on the users selection
def process_descriptive_analytics(descriptive_option):
    """
    This processes the number that the user inputs and calls the required functions.
    If the user doesn't enter an appropriate choice, it will ask them again until they do.
    """    
    while descriptive_option != "0":
        if descriptive_option == "1": # Calls the raw time series function from descriptive analytics module
            raw_time_series()       
            print("\n")
        elif descriptive_option == "2": # Calls the trend_line function from descriptive analytics module
            trend_line()
            print("\n")        
        elif descriptive_option == "3": # Calls the simple_moving_average function from descriptive analytics module
            simple_moving_average()
            print("\n")
        elif descriptive_option == "4": # Calls the cumulative_moving_average function from descriptive analytics module
            cumulative_moving_average()
            print("\n")                  
        elif descriptive_option == "5": # Calls the exponential_moving_average function from descriptive analytics module
            exponential_moving_average()
            print("\n")   
        elif descriptive_option == "6": # Calls the moving_average_convergence_divergence function from descriptive analytics module
            moving_average_convergence_divergence()
            print("\n")            
        elif descriptive_option == "7": # Help provided via text from a csv file
            display_help()
            print("\n")
        else:  # Wrong choice
            print("Invalid input, please try again.")
            print("\n")
            
        #Redisplay the user options
        display_descriptive_analytics()      
        #Gives a value to the option selected by a user
        descriptive_option = get_user_selection()


#This returns the predictive analytics menu and processes the choice using the function below
def predictive_analytics():

    display_predictive_analytics()
    predictive_option = get_user_selection()
    process_predictive_analytics(predictive_option)


#Performs the relevant operation based on the users selection
def process_predictive_analytics(predictive_option):
    """
    This processes the number that the user inputs and calls the required functions.
    If the user doesn't enter an appropriate choice, it will ask them again until they do.
    """
    while predictive_option != "0":
        if predictive_option == "1": # Calls the linear_regression function from predictive_analytics
            linear_regression()       
            print("\n")
        elif predictive_option == "2": #Calls the lstm_prediction function from predictive_analytics
            lstm_prediction()
            print("\n")                 
        elif predictive_option == "3": # Help provided via text from a csv file
            display_help()
            print("\n")
        else:  # Wrong choice
            print("Invalid input, please try again.")
            print("\n")
            
        #Redisplay the user options
        display_predictive_analytics()     
        #Gives a value to the option selected by a user
        predictive_option = get_user_selection()


#Calls the relevant functions to run the application
def main():
  
    company_list = import_company_list()
    
    display_welcome()
    
    display_main_menu()
    
    option = get_user_selection()
    
    process_selection(option, company_list)
    

    
if __name__ == '__main__':
    main()

