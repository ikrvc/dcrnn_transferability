import pandas as pd
import numpy as np
import runpy
import sys
import time

from lib import metrics

"""Code for the error testing of the graphs selected by one of the graph_selection methods"""

#PARAMETERS
sensor_ids_filename = 'data/sensor_graph/test_sensors.txt'
dataset_filename = 'data/pems-bay.h5'
distances_filename = 'data/sensor_graph/distances_bay_2017.csv'
input_file = 'results/simulated_annealing_results_big_abssum0.csv'
output_file = 'results/errors_of_graphs_big_abssum0.csv'
adj_mx_filename = 'data/sensor_graph/adj_mx_test.pkl'
test_config_file = 'data/model/pretrained/TEST/config.yaml'
subset_dataset_filename = 'data/testing.h5'




def run_module_with_args(module_name, args):
    # Save the original sys.argv
    original_argv = sys.argv
    try:
        # Set sys.argv to mimic command-line execution
        sys.argv = [''] + args
        # Execute the module
        runpy.run_module(module_name, run_name="__main__")
    finally:
        # Restore the original sys.argv
        sys.argv = original_argv


def calculate_error(n):
    # Load the .npz file (update file path accordingly)
    file_path = 'data/dcrnn_predictions.npz'
    data = np.load(file_path)

    # Extract predictions and ground truths
    prediction = data['prediction'][n]
    truth = data['truth'][n]

    error = metrics.calculate_metrics(prediction, truth, 0)
    return error


if __name__ == '__main__':
    dataset = pd.read_hdf(dataset_filename)
    testing_datasets = pd.read_csv(input_file)
    id_list_array = testing_datasets['Sensors']
    testing_datasets['Errors'] = np.empty(len(id_list_array), dtype=object)
    testing_datasets['Errors_0'] = np.empty(len(id_list_array), dtype=object)
    testing_datasets['Errors_15'] = np.empty(len(id_list_array), dtype=object)

    for graph_n, id_string in enumerate(id_list_array.values):
        start = time.time()

        with open(sensor_ids_filename, 'w') as file:
            file.write(id_string)

        id_list = [int(i) for i in id_string.split(',')]
        filtered_dataset = dataset[id_list]
        filtered_dataset.to_hdf(subset_dataset_filename, key='subregion_test', mode='w')
        run_module_with_args('scripts.generate_training_data',
                             ['--output_dir', 'data/TEST',
                              '--traffic_df_filename', subset_dataset_filename])
        run_module_with_args('scripts.gen_adj_mx',
                             ['--sensor_ids_filename', sensor_ids_filename,
                              '--distances_filename', distances_filename,
                              '--normalized_k', '0.1',
                              '--output_pkl_filename', adj_mx_filename])
        run_module_with_args('run_demo_pytorch', ['--config_filename', test_config_file])
        error = calculate_error(11)
        error0 = calculate_error(0)
        error15 = calculate_error(2)
        print(error)
        print(error0)
        # Calculating errors
        values = testing_datasets['Errors'].to_numpy()
        values[graph_n] = ','.join([str(x) for x in error])
        testing_datasets['Errors'] = values

        values = testing_datasets['Errors_0'].to_numpy()
        values[graph_n] = ','.join([str(x) for x in error0])
        testing_datasets['Errors_0'] = values

        values = testing_datasets['Errors_15'].to_numpy()
        values[graph_n] = ','.join([str(x) for x in error15])
        testing_datasets['Errors_15'] = values
        testing_datasets.to_csv(output_file)
        end = time.time()
        print('Graph testing time was: ', end-start, ' ms')

