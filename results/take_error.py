import numpy as np
import pandas as pd
import math
import scipy.stats as stats

"""
This code is used to calculate average error and standart error
"""
#PARAMETERS
file_path = 'errors_of_graphs.csv'

if __name__ == '__main__':
    data = pd.read_csv(file_path)
    # Extract the MAE from the Errors column
    data['MAE'] = data['Errors'].apply(lambda x: float(x.split(',')[0]))
    data['RMSE'] = data['Errors'].apply(lambda x: float(x.split(',')[2]))

    sample_size = len(data['MAE'])
    sample_avg = np.average(data['MAE'])
    squared_deviations = [(x - sample_avg) ** 2 for x in data['MAE']]
    sample_std_dev = math.sqrt(sum(squared_deviations) / (len(data['MAE']) - 1))
    sample_std = np.std(data['MAE'])

    standard_error = sample_std / math.sqrt(sample_size)

    z_score = stats.norm.ppf(0.975)
    margin_of_error = z_score * standard_error

    confidence_interval_lower = sample_avg - margin_of_error
    confidence_interval_upper = sample_avg + margin_of_error

    sample_avg_rmse = np.average(data['RMSE'])
    print('Sample avg RMSE: ', sample_avg_rmse)
    print('Sample avg MAE: ', sample_avg)
    print('Margin of error: ', margin_of_error)
    print('Standard error: ', standard_error)
