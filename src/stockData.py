import pandas as pd
import yfinance as yf
import datetime


def getStockData(start, end, ticker):
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
            stock['Name'] = ticker
            stock_final = stock_final.append(stock, sort=False)
    except Exception:
        None
    return stock_final

def getStockPrice(date, ticker):
    # fetch data by interval (including intraday if period < 60 days)
    # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    # (optional, default is '1d')
    # start = datetime.datetime.strptime(date, "%Y-%m-%d")
    start = date
    end = start + datetime.timedelta(days=1)
    stock = yf.download(ticker, start=start, end=end)
    return stock.Close


# getStockPrice("2020-01-06", "GME")