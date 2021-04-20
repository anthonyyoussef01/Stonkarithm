import pandas as pd
import yfinance as yf
import numpy as np
import datetime
from keras.models import Sequential
from keras.layers import Dense, Input


def getStockData(ticker, start, end):
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    # create empty dataframe
    stock_final = pd.DataFrame()
    try:
        #download the stock price
        stock = yf.download(ticker, start=start, end=end, progress=False)

        # append the individual stock prices
        if len(stock) == 0:
            None
        else:
            stock_final = stock_final.append(stock, sort=False)
    except Exception:
        None
    return stock_final


def build_dataset(ticker):
    fiveYear = pd.DataFrame(yf.download(ticker, period="5y", progress=False))
    # initial_date = fiveYear.iloc[0].name
    # end_date = fiveYear.iloc[fiveYear.size].name
    # currDate = initial_date + datetime.timedelta(30)
    size = len(fiveYear)-30
    idx = 30
    x = [0] * size
    y = [0] * size
    while idx <= size:
        stockDataOverLastMonth = fiveYear.iloc[idx-30:idx]
        x[idx-30] = stockDataOverLastMonth[["Volume", "Open"]].to_numpy()
        y[idx-30] = fiveYear.iloc[idx].Close
        # proceed to the next date
        idx = idx+1

    trainIdx = round((4/5) * len(fiveYear))
    xTrain= np.array(x[0:trainIdx])
    xValidate = np.array(x[trainIdx+1:len(x)])
    yTrain = np.array(y[0:trainIdx])
    yValidate = np.array(y[trainIdx+1:len(y)])

    return [xTrain, yTrain, xValidate, yValidate]


[xTrain, yTrain, xValidate, yValidate] = build_dataset("GME")
print(len(xTrain), len(xValidate))
# define the keras model
model = Sequential()
model.add(Dense(12,activation='relu', input_shape=(30,2)))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.summary()
# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit the keras model on the dataset
model.fit(xTrain, yTrain, epochs=150, batch_size=10)
# # evaluate the keras model
_, accuracy = model.evaluate(xTrain, yTrain)
print('Accuracy: %.2f' % (accuracy*100))