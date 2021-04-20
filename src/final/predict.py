from parameters import *
import matplotlib.pyplot as plt
import numpy as np

def getFinalData(model, data ):
    X_test = data["X_test"]
    y_test = data["y_test"]
    # predict price outputs
    y_pred = model.predict(X_test)
    # account for scaling
    if SCALE:
        y_test = np.squeeze(data["column_scaler"][TARGET_FEATURE].inverse_transform(np.expand_dims(y_test, axis=0)))
        y_pred = np.squeeze(data["column_scaler"][TARGET_FEATURE].inverse_transform(y_pred))

    test_df = data["test_df"]
    # add predicted future prices to the dataframe
    test_df[f"predicted_{TARGET_FEATURE}_{LOOKUP_STEP}"] = y_pred
    # add true future prices to the dataframe
    test_df[f"true_{TARGET_FEATURE}_{LOOKUP_STEP}"] = y_test
    # sort the dataframe by date
    test_df.sort_index(inplace=True)
    final_df = test_df
    # if price is predicted to go up, find total profit that would be made from buying
    buyProfit = lambda current, pred_future, true_future: true_future - current if pred_future > current else 0
    # if price is predicted to go down, find total profit that would be made from selling
    sellProfit = lambda current, pred_future, true_future: current - true_future if pred_future < current else 0
    final_df["buy_profit"] = list(map(buyProfit,
                                      final_df[TARGET_FEATURE],
                                      final_df[f"predicted_{TARGET_FEATURE}_{LOOKUP_STEP}"],
                                      final_df[f"true_{TARGET_FEATURE}_{LOOKUP_STEP}"]))
    final_df["sell_profit"] = list(map(sellProfit,
                                       final_df[TARGET_FEATURE],
                                       final_df[f"predicted_{TARGET_FEATURE}_{LOOKUP_STEP}"],
                                       final_df[f"true_{TARGET_FEATURE}_{LOOKUP_STEP}"]))

    return final_df

def predict(model, data):
    # retrieve the last sequence from data
    last_sequence = data["last_sequence"][-N_STEPS:]
    # expand dimension
    last_sequence = np.expand_dims(last_sequence, axis=0)
    # get the prediction (scaled from 0 to 1)
    prediction = model.predict(last_sequence)
    # get the price (by inverting the scaling)
    if SCALE:
        predicted_price = data["column_scaler"][TARGET_FEATURE].inverse_transform(prediction)[0][0]
    else:
        predicted_price = prediction[0][0]
    return predicted_price

def plot_graph(final_df):
    plt.plot(final_df[f'true_{TARGET_FEATURE}_{LOOKUP_STEP}'], c='b')
    plt.plot(final_df[f'predicted_{TARGET_FEATURE}_{LOOKUP_STEP}'], c='r')
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend(["Actual Price", "Predicted Price"])
    plt.title(ticker)
    plt.show()
