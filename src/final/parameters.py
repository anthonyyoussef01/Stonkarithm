import os
import time
from tensorflow.keras.layers import LSTM

# Pick ticker here
ticker = "SPY"
# set the start date you want to get stock and twitter data from
START_DATE = "01/01/2018"
# the ratio for testing to training 
TRAINING_RATIO = 0.2
# Briefly attempted to do a 7 day data test but found twitter api solution
# SEVEN_DAY = False
# if SEVEN_DAY:
#     TARGET_FEATURE = "close"
#     FEATURE_COLUMNS = ["close", "volume", "open", "high", "low"]
#     # start and end dates, format "month/day/year"
#     START_DATE = "04/10/2021"
#     END_DATE = "04/17/2021"
#     DAYS_AHEAD = 390
#     # Window size or the sequence length
#     N_DAYS_PRIOR = 195
# else:

# Lookup step, 1 is the next day
DAYS_AHEAD = 1
# features to use
FEATURE_COLUMNS = ["adjclose","close", "volume", "open", "high", "low", 'sentiment']
TARGET_FEATURE = "adjclose"
# Number of days prior to target, in this case 30 days
N_DAYS_PRIOR = 30

# date now
current_date = time.strftime("%Y-%m-%d")

# model parameters
N_LAYERS = 2
CELL = LSTM
UNITS = 200
BATCH_SIZE = 20
EPOCHS = 4

# Training parameters
DROPOUT = 0.45
LOSS = "mse"
OPTIMIZER = "adam"


# set up filename for saving data as csvs
ticker_data_filename = os.path.join("data", f"{ticker}_{current_date}.csv")
# model name to save, making it as unique as possible based on parameters
model_name = f"{current_date}_{ticker}-step-{DAYS_AHEAD}-layers-{N_LAYERS}"