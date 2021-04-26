from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
from data import *
from model import create_model

from predict import *

##################### TRAINING ########################
data = load_data_historical(ticker, N_DAYS_PRIOR, days_ahead=DAYS_AHEAD, training_ratio=TRAINING_RATIO,
                feature_columns=FEATURE_COLUMNS)

# save df in files
data["df"].to_csv(ticker_data_filename)

# construct the model
model = create_model(N_DAYS_PRIOR, len(FEATURE_COLUMNS), loss=LOSS, units=UNITS, cell=CELL, n_layers=N_LAYERS,
                    dropout=DROPOUT, optimizer=OPTIMIZER)

# a checkpoint object that stores the weights at each epoch to so ultimatley we will get the best weights
checkpointer = ModelCheckpoint(os.path.join("results", model_name + ".h5"), save_weights_only=True, save_best_only=True, verbose=1)
# figure out tensorboard later
tensorboard = TensorBoard(log_dir=os.path.join("logs", model_name))
# Training occurs here
model.fit(data["X_train"], data["Y_train"],
                batch_size=BATCH_SIZE,
                epochs=EPOCHS,
                validation_data=(data["X_test"], data["Y_test"]),
                callbacks=[checkpointer, tensorboard],
                verbose=1)

##################### EVALUATION ########################

# load optimal model weights from results folder
model_path = os.path.join("results", model_name) + ".h5"
model.load_weights(model_path)

# evaluate the model
loss, mse = model.evaluate(data["X_test"], data["Y_test"], verbose=0)
# calculate the mean absolute error (inverse scaling)
mean_squared_error = data["column_scaler"][TARGET_FEATURE].inverse_transform([[mse]])[0][0]


# get the final dataframe for the testing set
final_df = getFinalData(model, data)
print("\nfd", final_df, "\n")

# predict the future price
future_price = predict(model, data)

# we calculate the accuracy by counting the number of time we correctly
# predicted the price direction and made profit
accuracy_score = (len(final_df[final_df['sell_profit'] > 0]) + len(final_df[final_df['buy_profit'] > 0])) / len(final_df)
# calculate the buy profit
buy_profit_sum = final_df["buy_profit"].sum()
sell_profit_sum = final_df["sell_profit"].sum()
# total profit by adding sell & buy together
total_profit = buy_profit_sum + sell_profit_sum

# printing important values
print(f"Future price after {DAYS_AHEAD} days is {future_price:.2f}$")
print(f"{LOSS} loss:", loss)
print("Mean Squared Error:", mean_squared_error)
print("Accuracy:", accuracy_score)
print("Total buy profit:", buy_profit_sum)
print("Total sell profit:", sell_profit_sum)
print("Total profit:", total_profit)


# plot the graph for visualization
plot_results(final_df)

# save the final dataframe to the results folder
csv_results_folder = "csv-results"
csv_filename = os.path.join(csv_results_folder, model_name + ".csv")
final_df.to_csv(csv_filename)
