import os
import time
from tensorflow.keras.layers import LSTM

# whether to scale feature columns & output price as well
SCALE = True
scale_str = f"sc-{int(SCALE)}"
# test ratio size, 0.2 is 20%
TEST_SIZE = 0.2
SEVEN_DAY = False
if SEVEN_DAY:
    TARGET_FEATURE = "close"
    FEATURE_COLUMNS = ["close", "volume", "open", "high", "low"]
    # start and end dates, format "month/day/year"
    START_DATE = "04/10/2021"
    END_DATE = "04/17/2021"
    LOOKUP_STEP = 390
    # Window size or the sequence length
    N_STEPS = 195
else:
    # Lookup step, 1 is the next day
    LOOKUP_STEP = 1
    # features to use
    FEATURE_COLUMNS = ["adjclose", "volume", "open", "high", "low"]
    TARGET_FEATURE = "adjclose"
    START_DATE = "doesnt matter"
    END_DATE = "doesnt matter"
    # Window size or the sequence length
    N_STEPS = 30

# date now
date_now = time.strftime("%Y-%m-%d")
# model parameters
N_LAYERS = 2
CELL = LSTM
UNITS = 200
BATCH_SIZE = 10
EPOCHS = 2
# 40% dropout
DROPOUT = 0.4
# training parameters
# mean absolute error loss
# LOSS = "mae"
# huber loss
LOSS = "mse"
OPTIMIZER = "adam"
# Pick ticker here
ticker = "AMZN"
ticker_data_filename = os.path.join("data", f"{ticker}_{date_now}.csv")
# model name to save, making it as unique as possible based on parameters
model_name = f"{date_now}_{ticker}-\
{LOSS}-{OPTIMIZER}-{CELL.__name__}-seq-{N_STEPS}-step-{LOOKUP_STEP}-layers-{N_LAYERS}-units-{UNITS}"