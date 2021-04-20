from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
from data import *
from model import create_model

from predict import *

##################### TRAINING ########################
if SEVEN_DAY:
    data = load_data_7days(ticker, N_STEPS, scale=SCALE, lookup_step=LOOKUP_STEP, test_size=TEST_SIZE,
                                feature_columns=FEATURE_COLUMNS)
else:
    data = load_data_historical(ticker, N_STEPS, scale=SCALE, lookup_step=LOOKUP_STEP, test_size=TEST_SIZE,
                feature_columns=FEATURE_COLUMNS)

# save df in files
data["df"].to_csv(ticker_data_filename)

# construct the model
model = create_model(N_STEPS, len(FEATURE_COLUMNS), loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS,
                    dropout=DROPOUT, optimizer=OPTIMIZER)

# a checkpoint object that stores the weights at each epoch to so ultimatley we will get the best weights
checkpointer = ModelCheckpoint(os.path.join("results", model_name + ".h5"), save_weights_only=True, save_best_only=True, verbose=1)
# figure out tensorboard later
tensorboard = TensorBoard(log_dir=os.path.join("logs", model_name))
# Training occurs here
model.fit(data["X_train"], data["y_train"],
                batch_size=BATCH_SIZE,
                epochs=EPOCHS,
                validation_data=(data["X_test"], data["y_test"]),
                callbacks=[checkpointer, tensorboard],
                verbose=1)

##################### EVALUATION ########################

# load optimal model weights from results folder
model_path = os.path.join("results", model_name) + ".h5"
model.load_weights(model_path)

# evaluate the model
loss, mse = model.evaluate(data["X_test"], data["y_test"], verbose=0)
# calculate the mean absolute error (inverse scaling)
if SCALE:
    mean_squared_error = data["column_scaler"][TARGET_FEATURE].inverse_transform([[mse]])[0][0]
else:
    mean_squared_error = mse

# get the final dataframe for the testing set
final_df = getFinalData(model, data)
print("\nfd", final_df, "\n")

# predict the future price
future_price = predict(model, data)

# we calculate the accuracy by counting the number of positive profits
accuracy_score = (len(final_df[final_df['sell_profit'] > 0]) + len(final_df[final_df['buy_profit'] > 0])) / len(final_df)
# calculating total buy & sell profit
total_buy_profit  = final_df["buy_profit"].sum()
total_sell_profit = final_df["sell_profit"].sum()
# total profit by adding sell & buy together
total_profit = total_buy_profit + total_sell_profit

# printing metrics
print(f"Future price after {LOOKUP_STEP} days is {future_price:.2f}$")
print(f"{LOSS} loss:", loss)
print("Mean Squared Error:", mean_squared_error)
print("Accuracy score:", accuracy_score)
print("Total buy profit:", total_buy_profit)
print("Total sell profit:", total_sell_profit)
print("Total profit:", total_profit)
print("Profit per trade:", profit_per_trade)

# plot true/pred prices graph
plot_graph(final_df)

print(final_df.tail(10))
# save the final dataframe to csv-results folder
csv_results_folder = "csv-results"
csv_filename = os.path.join(csv_results_folder, model_name + ".csv")
final_df.to_csv(csv_filename)
