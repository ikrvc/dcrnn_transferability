import pandas as pd

"""
This code is used to create a dataset for a subgraph
"""

#PARAMETERS
"""
dataset_file - file of full dataset
sensor_id_file - file with subgraph sensor ids
subgraph_file - subgraph dataset saving file
"""
dataset_file = "../data/pems-bay.h5"
sensor_id_file = "../data/sensor_graph/test_sensors.txt"
subgraph_file = '../data/testing.h5'


def read_ids_to_array(file_path):
    with open(file_path, 'r') as file:
        # Read the single line containing the IDs
        content = file.read()

        # Remove any trailing newline characters and split by comma
        id_list = content.strip().split(',')

    return id_list


if __name__ == '__main__':
    #Full dataset
    dataset = pd.read_hdf(dataset_file)
    #Subset sensor ids (separated by coma)
    id_list = read_ids_to_array(sensor_id_file)
    id_list = [int(i) for i in id_list]
    filtered_dataset = dataset[id_list]
    #Save subset dataset
    filtered_dataset.to_hdf(subgraph_file, key='subregion_test', mode='w')
    print(filtered_dataset)

