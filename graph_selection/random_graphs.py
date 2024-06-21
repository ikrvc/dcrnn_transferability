from simulated_annealing_helper_functions import read_ids_to_array, initialize_sensors, save_results_to_csv

"""Random graph selection"""

#PARAMETERS
num_sensors = 10
num_selected = 200
bay_id_file = "../data/sensor_graph/graph_sensor_ids_bay.txt"
export_file = '../results/random_sensors_small.csv'


if __name__ == '__main__':
    bay_id_list = read_ids_to_array(bay_id_file)

    results = []
    for i in range(num_selected):
        results.append(initialize_sensors(bay_id_list, num_sensors))

    save_results_to_csv(results, export_file)