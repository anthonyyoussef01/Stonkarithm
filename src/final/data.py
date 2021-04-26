from sklearn import preprocessing
from yahoo_fin import stock_info as si
from collections import deque
import numpy as np
from sentiment import *
from parameters import START_DATE


def load_data_historical(ticker, n_days_prior=30, days_ahead=1,
                training_ratio=0.2, feature_columns=['adjclose', 'volume', 'open','close', 'high', 'low', 'sentiment']):
    # get all data from ticker since twitter was created
    df = si.get_data(ticker, start_date=START_DATE)
    # this will contain all the elements we want to return from this function
    result = {}
    # add the sentiment as a column
    df["sentiment"] = getTwitterSentimentScore(df.index.values)
    # we will also store the original stock df
    result['df'] = df.copy()
    # add date as a column
    df["date"] = df.index
    print("done with adding sentiment")
    column_scaler = {}
    # scale the data to be from 0 to 1 so ml can run faster,
    for column in feature_columns:
        scaler = preprocessing.MinMaxScaler()
        df[column] = scaler.fit_transform(np.expand_dims(df[column].values, axis=1))
        column_scaler[column] = scaler
    # add the MinMaxScaler instances to the result returned
    result["column_scaler"] = column_scaler
    # add the future results by shifting by `days_ahead`
    df['future'] = df['adjclose'].shift(-days_ahead)
    # last `days_ahead` columns contains NaN in future column so get them and store them
    last_sequence = np.array(df[feature_columns].tail(days_ahead))
    # drop the invalid Nan values
    df.dropna(inplace=True)
    sequence_data = []
    # set up sequences to track the data for the number of steps before the target date
    sequences = deque(maxlen=n_days_prior)
    for entry, target in zip(df[feature_columns + ["date"]].values, df['future'].values):
        sequences.append(entry)
        # once you have reached the last step add the target price to sequences
        if len(sequences) == n_days_prior:
            sequence_data.append([np.array(sequences), target])
    # get the last sequence by appending the last `n_step` sequence with `days_ahead` sequence
    # this last_sequence will be used to predict future stock prices that are not available in the dataset
    last_sequence = list([s[:len(feature_columns)] for s in sequences]) + list(last_sequence)
    last_sequence = np.array(last_sequence).astype(np.float32)
    # save last sequence in result
    result['last_sequence'] = last_sequence
    # initialize x and y for data
    X, Y = [], []
    for s, t in sequence_data:
        X.append(s)
        Y.append(t)
    # convert to numpy arrays
    X = np.array(X)
    Y = np.array(Y)
    # split the dataset into training & testing/validation sets by date
    train_samples = int((1 - training_ratio) * len(X))
    result["X_train"] = X[:train_samples]
    result["Y_train"] = Y[:train_samples]
    result["X_test"] = X[train_samples:]
    result["Y_test"] = Y[train_samples:]

    # get the list of test set dates
    dates = result["X_test"][:, -1, -1]
    # retrieve test features from the original dataframe
    result["test_df"] = result["df"].loc[dates]
    # remove duplicated dates in the testing dataframe
    result["test_df"] = result["test_df"][~result["test_df"].index.duplicated(keep='first')]
    # remove dates from the training/testing sets & convert to float32
    result["X_train"] = result["X_train"][:, :, :len(feature_columns)].astype(np.float32)
    result["X_test"] = result["X_test"][:, :, :len(feature_columns)].astype(np.float32)
    return result

#used for testing
#load_data_historical("AAPL")

# created to try to predict with 7 day data, ended up not using
# def load_data_7days(ticker, n_days_prior=190, scale=True, days_ahead=390,
#                 test_size=0.2, feature_columns=['open', 'volume', 'close', 'high', 'low']):
#     # 390 is the amount of minutes in one market day
#     # get data in last 7 days by minute
#     df = si.get_data(ticker, start_date=START_DATE, end_date=END_DATE, interval="1m")
#     # this will contain all the elements we want to return from this function
#     result = {}
#     # we will also return the original dataframe itself
#     result['df'] = df.copy()
#     # make sure that the passed feature_columns exist in the dataframe
#     for col in feature_columns:
#         assert col in df.columns, f"'{col}' does not exist in the dataframe."
#     # add date-minute as a column
#     df["date-minute"] = df.index
#     if scale:
#         column_scaler = {}
#         # scale the data (prices) from 0 to 1
#         for column in feature_columns:
#             scaler = preprocessing.MinMaxScaler()
#             df[column] = scaler.fit_transform(np.expand_dims(df[column].values, axis=1))
#             column_scaler[column] = scaler
#         # add the MinMaxScaler instances to the result returned
#         result["column_scaler"] = column_scaler
#     # add the target column (label) by shifting by `days_ahead` in this case it is 1440 which is 24 hours in minutes
#     df['future'] = df['close'].shift(-days_ahead)
#     # last `days_ahead` columns contains NaN in future column
#     # get them before droping NaNs
#     last_sequence = np.array(df[feature_columns].tail(days_ahead))
#     # drop NaNs
#     df.dropna(inplace=True)
#     sequence_data = []
#     # set sequences to
#     sequences = deque(maxlen=n_days_prior)
#     for entry, target in zip(df[feature_columns + ["date-minute"]].values, df['future'].values):
#         sequences.append(entry)
#         if len(sequences) == n_days_prior:
#             sequence_data.append([np.array(sequences), target])
#     # get the last sequence by appending the last `n_step` sequence with `days_ahead` sequence
#     # for instance, if n_days_prior=50 and days_ahead=10, last_sequence should be of 60 (that is 50+10) length
#     # this last_sequence will be used to predict future stock prices that are not available in the dataset
#     last_sequence = list([s[:len(feature_columns)] for s in sequences]) + list(last_sequence)
#     last_sequence = np.array(last_sequence).astype(np.float32)
#     # add to result
#     result['last_sequence'] = last_sequence
#     # construct the X's and y's
#     X, y = [], []
#     for seq, target in sequence_data:
#         X.append(seq)
#         y.append(target)
#     # convert to numpy arrays
#     X = np.array(X)
#     y = np.array(y)
#     # split the dataset into training & testing sets by date
#     train_samples = int((1 - test_size) * len(X))
#     result["X_train"] = X[:train_samples]
#     result["y_train"] = y[:train_samples]
#     result["X_test"] = X[train_samples:]
#     result["y_test"] = y[train_samples:]
#
#     # get the list of test set dates
#     dates = result["X_test"][:, -1, -1]
#     # retrieve test features from the original dataframe
#     result["test_df"] = result["df"].loc[dates]
#     # remove duplicated dates in the testing dataframe
#     result["test_df"] = result["test_df"][~result["test_df"].index.duplicated(keep='first')]
#     # remove dates from the training/testing sets & convert to float32
#     result["X_train"] = result["X_train"][:, :, :len(feature_columns)].astype(np.float32)
#     result["X_test"] = result["X_test"][:, :, :len(feature_columns)].astype(np.float32)
#     return result

