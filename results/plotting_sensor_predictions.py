import numpy as np
import matplotlib.pyplot as plt

"""
This code is used to plot the predictions of the sensor.
Here data_path show the file with predictions.
"""
#PARAMETERS
data_path = '../data/dcrnn_predictions_test_big_404586.npz'



if __name__ == '__main__':
    data = np.load(data_path)
    prediction = data['prediction']
    truth = data['truth']

    # Select a specific timestep and feature
    timestep = 11
    sensor = 40

    # Extract predictions and truths for the chosen timestep and feature
    predictions_selected = prediction[timestep,4500:5000, sensor]
    truths_selected = truth[timestep, 4500:5000, sensor]

    # Plot predictions vs. truths
    plt.figure(figsize=(12, 6))
    plt.plot(truths_selected, label='Ground Truth', color='blue')
    plt.plot(predictions_selected, label='Prediction', color='red', linestyle='dashed')
    plt.xlabel('Amount of timestamps (one is 5 min)', fontsize=14)
    plt.ylabel('Speed (mph)', fontsize=14)
    # plt.title(f'50-sensor DCRNN prediction for sensor 414284')
    plt.tick_params(axis='both', which='major', labelsize=14)
    plt.tick_params(axis='both', which='minor', labelsize=14)
    plt.legend(fontsize=14)
    plt.ylim(54, 68)
    plt.show()