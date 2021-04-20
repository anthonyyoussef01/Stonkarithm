import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional

def create_model(sequence_length, n_features, units=256, cell=LSTM, n_layers=2, dropout=0.3,
                loss='mean_squared_error', optimizer="rmsprop"):
    model = Sequential()
    for i in range(n_layers):
        if i == 0:
            model.add(Bidirectional(cell(units, return_sequences=True), batch_input_shape=(None, sequence_length, n_features)))
        elif i == n_layers - 1:
            model.add(Bidirectional(cell(units, return_sequences=False)))
        else:
            # hidden layers
            model.add(Bidirectional(cell(units, return_sequences=True)))
        # add dropout after each layer
        model.add(Dropout(dropout))
    model.add(Dense(1, activation="linear"))
    model.compile(loss=loss, metrics=['mean_squared_error'], optimizer=optimizer)
    return model
