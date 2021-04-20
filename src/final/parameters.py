import os
import time
from tensorflow.keras.layers import LSTM

# whether to scale feature columns & output price as well
SCALE = True
scale_str = f"sc-{int(SCALE)}"
# test ratio size, 0.2 is 20%
TEST_SIZE = 0.2
SEVEN_DAY = True
if SEVEN_DAY:
    TARGET_FEATURE = "close"
    FEATURE_COLUMNS = ["close", "volume", "open", "high", "low"]
    # start and end dates, format "month/day/year"
    START_DATE = "04/10/2021"
    END_DATE = "04/17/2021"
    LOOKUP_STEP = 390
    # Window size or the sequence length
    N_STEPS = 5
else:
    # Lookup step, 1 is the next day
    LOOKUP_STEP = 1
    # features to use
    FEATURE_COLUMNS = ["adjclose", "volume", "open", "high", "low"]
    TARGET_FEATURE = "adjclose"
    # Window size or the sequence length
    N_STEPS = 30

# date now
date_now = time.strftime("%Y-%m-%d")
### model parameters
N_LAYERS = 2
# LSTM cell
CELL = LSTM
# 150 LSTM neurons
UNITS = 200
# 40% dropout
DROPOUT = 0.4
# whether to use bidirectional RNNs
BIDIRECTIONAL = True
### training parameters
# mean absolute error loss
# LOSS = "mae"
# huber loss
LOSS = "mse"
OPTIMIZER = "adam"
BATCH_SIZE = 5
EPOCHS = 10
# Pick ticker here
ticker = "AMZN"
ticker_data_filename = os.path.join("data", f"{ticker}_{date_now}.csv")
# model name to save, making it as unique as possible based on parameters
model_name = f"{date_now}_{ticker}-\
{LOSS}-{OPTIMIZER}-{CELL.__name__}-seq-{N_STEPS}-step-{LOOKUP_STEP}-layers-{N_LAYERS}-units-{UNITS}"
if BIDIRECTIONAL:
    model_name += "-b"