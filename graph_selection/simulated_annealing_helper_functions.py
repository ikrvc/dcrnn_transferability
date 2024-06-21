import pandas as pd
import numpy as np


def read_ids_to_array(file_path):
    """
    Used to read sensor ids from comma-separated file
    """
    with open(file_path, 'r') as file:
        # Read the single line containing the IDs
        content = ' '.join(file.readlines())
        # Remove any trailing newline characters and split by comma
        id_list = content.strip().split(',')
    return id_list

def save_results_to_csv(results, filename):
    """
    Used to save results into specified csv file
    """
    # Convert results to a DataFrame
    df = pd.DataFrame(results, columns=['Cost', 'Sensors'])
    # Convert the list of sensors to a comma-separated string if they aren't already
    df['Sensors'] = df['Sensors'].apply(lambda x: ','.join(map(str, x)))
    # Save to CSV
    df.to_csv(filename, index=False)

def initialize_sensors(all_sensors, num_select):
    """Random sensor initialization"""
    return np.random.choice(all_sensors, num_select, replace=False)


def get_adjacency_matrix(distance_df, sensor_ids, inf_val=40000):
    """
    Creation of the graph adjacency matrix
    :param distance_df: DataFrame with three columns: [from, to, distance].
    :param sensor_ids: List of sensor ids.
    :param inf_val: mask value
    :return: Adjacency matrix.
    """
    num_sensors = len(sensor_ids)

    # Build sensor id to index map
    sensor_id_to_ind = {sensor_id: i for i, sensor_id in enumerate(sensor_ids)}

    # Initialize distance matrix with a large value
    dist_mx = np.full((num_sensors, num_sensors), inf_val, dtype=np.float32)

    # Fill the matrix with distances
    valid_indices = distance_df[distance_df['from'].isin(sensor_id_to_ind) &
                                distance_df['to'].isin(sensor_id_to_ind)]

    from_indices = valid_indices['from'].map(sensor_id_to_ind)
    to_indices = valid_indices['to'].map(sensor_id_to_ind)
    distances = valid_indices['cost'].values

    dist_mx[from_indices, to_indices] = distances

    return dist_mx
