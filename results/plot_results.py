import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr


"""
This code is used to plot the correlation.
"""
#PARAMETERS
file_path = 'errors_of_graphs_big_cos40000.csv'

if __name__ == '__main__':
    data = pd.read_csv(file_path)

    # Extract the MAE from the Errors column
    data['MAE'] = data['Errors'].apply(lambda x: float(x.split(',')[0]))

    # Calculate Pearson correlation
    pearson_corr, _ = pearsonr(data['Cost'], data['MAE'])

    # Calculate the regression line
    slope, intercept = np.polyfit(data['Cost'], data['MAE'], 1)
    regression_line = slope * data['Cost'] + intercept

    # Plotting Cost vs. MAE with regression line
    plt.figure(figsize=(10, 6))
    plt.scatter(data['Cost'], data['MAE'], color='blue', alpha=0.5, label='Data points')
    plt.plot(data['Cost'], regression_line, color='red', label='Regression line')
    # plt.text(0.05, 0.95, f'Pearson Correlation: {pearson_corr:.2f}',
    #          transform=plt.gca().transAxes, fontsize=14, verticalalignment='top')
    plt.xlabel('Cosine distance with 40000 for mask', fontsize=14)
    plt.ylabel('Mean Absolute Error (MAE)', fontsize=14)
    plt.legend(fontsize=14)
    plt.grid(True)

    # Increase tick label size
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)

    plt.savefig(f'./pictures/correlation/{file_path[:-4]}_plot.png')
    plt.show()
