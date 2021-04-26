from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional

# create model for neural network, using bidirectional layers and LSTM activation function
def create_model(sequence_length, n_features, units=256, cell=LSTM, n_layers=2, dropout=0.3,
                loss='mean_squared_error', optimizer="adam"):
    # use sequential model from keras
    model = Sequential()
    # create total num of layers
    for i in range(n_layers):
        # for the first layer
        if i == 0:
            model.add(Bidirectional(cell(units, return_sequences=True), batch_input_shape=(None, sequence_length, n_features)))
        # for the last layer
        elif i == n_layers - 1:
            model.add(Bidirectional(cell(units, return_sequences=False)))
        # for all other layers
        else:
            # hidden layers
            model.add(Bidirectional(cell(units, return_sequences=True)))
        # add dropout after all layers
        model.add(Dropout(dropout))
    # add one final linera layer to help us predict the outcome
    model.add(Dense(1, activation="linear"))
    # compile our model so it is ready to train
    model.compile(loss=loss, metrics=['mean_squared_error'], optimizer=optimizer)
    return model
