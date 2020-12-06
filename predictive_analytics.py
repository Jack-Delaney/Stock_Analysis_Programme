# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Wed Dec 2 23:08:22 2020

@author: JDela
"""
#import packages
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import datetime as dt
import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
import math
import pandas_datareader as web
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import datetime 


#This returns the stock data from the csv files that the user downloads, for analytical purposes
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
        
    stock_df = pd.read_csv(symbol + ".csv")
    
    return symbol, company, stock_df


#This linear regression function was adapted from the tutorial linked on brightspace, found at https://medium.com/@srkhedkar/stock-market-prediction-using-python-article-1-the-straight-line-c23f26579b4d
def linear_regression():
    """
    This function plots the different price points against whatever date range is found in the csv file.
    Then it plots the line of best fit (or least error) for the time range, before continuing the line into the
    future, thus indicating where the linear regression formula predicts the price to be at that point.
    """
    symbol, company, stock_df = get_csv_data()
    
    #setting index as date
    stock_df['Date'] = pd.to_datetime(stock_df.Date)
    stock_df.index = stock_df['Date']
    
    #converting dates into number of days as dates cannot be passed directly to any regression model
    stock_df.index = (stock_df.index - pd.to_datetime('1970-01-01')).days
    
    # Convert the pandas series into numpy array, we need to further massage it before sending it to regression model
    y = np.asarray(stock_df['Close'])
    x = np.asarray(stock_df.index.values)
    
    # Model initialization
    # by default the degree of the equation is 1.
    # Hence the mathematical model equation is y = mx + c, which is an equation of a line.
    regression_model = LinearRegression()
    
    # Fit the data(train the model)
    regression_model.fit(x.reshape(-1, 1), y.reshape(-1, 1))
    
    # Prediction for historical dates. Let's call it learned values.
    y_learned = regression_model.predict(x.reshape(-1, 1))
    
    #ensures that the number of days entered is a positive integer
    validation = None
    while validation is None:
        try:
            days = int(input('Please enter how many days into the future you want your predicted price to be: '))
            validation = days
            if days < 0:
                validation = None
                print('Please pick a positive number')
        except:
            print('Please enter an integer value')    
    
    # Now, add future dates to the date index and pass that index to the regression model for future prediction.
    # As we have converted date index into a range index, hence, here we just need to add a specified number of 'days'
    # to the previous index. x[-1] gives the last value of the series.
    newindex = np.asarray(pd.RangeIndex(start=x[-1], stop=x[-1] + days))
    
    # Prediction for future dates. Let's call it predicted values.
    y_predict = regression_model.predict(newindex.reshape(-1, 1))
    
    #print the last predicted value
    print ('Closing price in '+str(days)+' days would be around ', y_predict[-1])
    
    #convert the days index back to dates index for plotting the graph
    x = pd.to_datetime(stock_df.index, origin='1970-01-01', unit='D')
    future_x = pd.to_datetime(newindex, origin='1970-01-01', unit='D')
    
    #setting figure size
    from matplotlib.pylab import rcParams
    rcParams['figure.figsize'] = 20,10
    
    #plot the actual data
    plt.figure(figsize=(16,8))
    plt.plot(x,stock_df['Close'], label='Close Price History')
    
    #plot the regression model
    plt.plot(x,y_learned, color='r', label='Mathematical Model')
    
    #plot the future predictions
    plt.plot(future_x,y_predict, color='g', label='Future predictions')
    
    plt.suptitle('Close Price Predictions for ' + company, fontsize=16)
    
    fig = plt.gcf()
    fig.canvas.set_window_title('Close Price Predictions for ' + company)
    
    plt.legend()
    plt.show()
    
    
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
    

#This returns the integer difference between two days, code adapted from https://stackoverflow.com/questions/8419564/difference-between-two-dates-in-python    
def days_between(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)

    
#This long short term memory model was adapted from the following tutorial https://randerson112358.medium.com/stock-price-prediction-using-python-machine-learning-e82a039ac2bb
def lstm_prediction():
    symbol, company, stock_df = get_csv_data()
    

    #Visualize the closing price history
    plt.figure(figsize=(16,8))
    plt.title('Close Price History')
    plt.plot(stock_df['Close'])
    plt.xlabel('Date',fontsize=18)
    plt.ylabel('Close Price USD ($)',fontsize=18)
    plt.show()
    
    #setting index as date
    #df['Date'] = pd.to_datetime(df.Date)
    stock_df.index = stock_df['Date']
    
    #Create a new dataframe with only the 'Close' column
    data = stock_df.filter(['Close'])
    #Converting the dataframe to a numpy array
    dataset = data.values
    #Get /Compute the number of rows to train the model on
    training_data_len = math.ceil( len(dataset) *.8) 
    
    #Scale the all of the data to be values between 0 and 1 
    scaler = MinMaxScaler(feature_range=(0, 1)) 
    scaled_data = scaler.fit_transform(dataset)
    
    #Create the scaled training data set 
    train_data = scaled_data[0:training_data_len  , : ]
    #Split the data into x_train and y_train data sets
    x_train=[]
    y_train = []
    for i in range(60,len(train_data)):
        x_train.append(train_data[i-60:i,0])
        y_train.append(train_data[i,0])
        
    #Convert x_train and y_train to numpy arrays
    x_train, y_train = np.array(x_train), np.array(y_train)    
    
    #Reshape the data into the shape accepted by the LSTM
    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
    
    #Build the LSTM network model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True,input_shape=(x_train.shape[1],1)))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=25))
    model.add(Dense(units=1))
    
    #Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    #Train the model
    model.fit(x_train, y_train, batch_size=1, epochs=1)
    
    #Test data set
    test_data = scaled_data[training_data_len - 60: , : ]
    
    #Create the x_test and y_test data sets
    x_test = []
    y_test =  dataset[training_data_len : , : ] #Get all of the rows from a certain index (80% of the whole dataset) to the rest and all of the columns (in this case it's only column 'Close')
    for i in range(60,len(test_data)):
        x_test.append(test_data[i-60:i,0])
        
    #Convert x_test to a numpy array 
    x_test = np.array(x_test)
    
    #Reshape the data into the shape accepted by the LSTM
    x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))
    
    #Getting the models predicted price values
    predictions = model.predict(x_test) 
    predictions = scaler.inverse_transform(predictions)#Undo scaling
    
    #Calculate/Get the value of RMSE
    rmse=np.sqrt(np.mean(((predictions- y_test)**2)))
    print('\nThe models RMSE value is: ' + str(rmse))
    
    #Plot/Create the data for the graph
    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions
    
    #Visualize the data
    plt.figure(figsize=(16,8))
    plt.title('LSTM Model for ' + company)
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close Price USD ($)', fontsize=18)
    plt.plot(train['Close'])
    plt.plot(valid[['Close', 'Predictions']])
    plt.legend(['Train', 'Value', 'Predictions'], loc='lower right')
    plt.show()
    
    #Show the valid and predicted prices
    print("\nThe following table displays actual Close versus Predicted close.")
    print(valid)
    
    end = datetime.datetime.today().strftime('%Y-%m-%d')
    
    #This uses the validate() function to ensure date formats are correct
    start_validation = None
    while start_validation is None:
        try:
            start = input("""
This model predicts tomorrows closing price. Choose a time range larger than 60 days.                          
Please enter time ranges in the format (YYYY-MM-DD). Example: 2019-12-31. 
Please enter a starting date: """)            
            validate(start)
            if days_between(end, start) > 60:
                start_validation = start
            else:
                print('Time range must be larger than 60 days')
                start_validation = None
        except ValueError:
            print('Please make sure it is in the following format: YYYY-MM-DD')
    
    
    #Get the quote
    stock_quote = web.DataReader(symbol, data_source='yahoo', start=start, end=end)
    #Create a new dataframe
    new_df = stock_quote.filter(['Close'])
    #Get the last 60 day closing price 
    last_60_days = new_df[-60:].values
    #Scale the data to be values between 0 and 1
    last_60_days_scaled = scaler.transform(last_60_days)
    #Create an empty list
    X_test = []
    #Append teh past 60 days
    X_test.append(last_60_days_scaled)
    #Convert the X_test data set to a numpy array
    X_test = np.array(X_test)
    #Reshape the data
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    #Get the predicted scaled price
    pred_price = model.predict(X_test)
    #undo the scaling 
    pred_price = scaler.inverse_transform(pred_price)
    print("Tomorrow's predicted closing prices is below:")
    print(pred_price)

    
    # #Get the quote - checks the models value by obtaining the actual value
    # stock_quote2 = web.DataReader(symbol, data_source='yahoo', start='2020-12-02', end='2020-12-02')
    # print(stock_quote2['Close'])    