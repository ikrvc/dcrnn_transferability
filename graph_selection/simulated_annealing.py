from graph_selection.distance_functions import dist
from lib.utils import load_graph_data
from graph_selection.simulated_annealing_helper_functions import *

"""This code runs """



#PARAMETERS
dist_mode = 'fro'
adj_mx = '../data/sensor_graph/adj_mx_50subset.pkl'
results_file = '../results/simulated_annealing_results_big_abssum0.csv'
num_buckets = 50
num_selected = 50
iterations = 100000
temp = 10000
inf_val = 0


def simulated_annealing(distances, template_matrix, total_sensor_ids, dist_mode, num_selected=50, iterations=10000, temp=100,
                        cooling_rate=0.95, inf_val=40000):
    best_cost = 100000000
    best_ids = []
    current_solution = initialize_sensors(total_sensor_ids, num_selected)
    current_adj_matrix = get_adjacency_matrix(distances, current_solution, inf_val=inf_val)
    current_cost = dist(current_adj_matrix, template_matrix, dist_mode)

    for i in range(iterations):
        new_solution = neighbor(current_solution, total_sensor_ids)
        new_adj_matrix = get_adjacency_matrix(distances, new_solution, inf_val=inf_val)
        new_cost = dist(new_adj_matrix, template_matrix, dist_mode)

        if new_cost < current_cost or np.random.rand() < np.exp((current_cost - new_cost) / temp):
            current_solution = new_solution
            current_cost = new_cost
            if new_cost < best_cost:
                best_cost = new_cost
                best_ids = new_solution
        temp *= cooling_rate

    return best_cost, best_ids

def neighbor(solution, total_sensors):
    new_solution = solution.copy()
    remove_index = np.random.randint(len(solution))
    new_sensor = np.random.choice(total_sensors)
    while np.isin(new_sensor, new_solution):
        new_sensor = np.random.choice(total_sensors)
    new_solution[remove_index] = new_sensor
    return new_solution

if __name__ == '__main__':
    template_sensor_ids, template_sensor_id_to_ind, _ = load_graph_data(adj_mx)
    distance_df = pd.read_csv('../data/sensor_graph/distances_bay_2017.csv', dtype={'from': 'str', 'to': 'str'})
    distance_df_la = pd.read_csv('../data/sensor_graph/distances_la_2012.csv', dtype={'from': 'str', 'to': 'str'})
    bay_id_list = read_ids_to_array("../data/sensor_graph/graph_sensor_ids_bay.txt")
    la_id_list = read_ids_to_array("../data/sensor_graph/graph_sensor_ids.txt")
    template_adj_mx = get_adjacency_matrix(distance_df_la, template_sensor_ids, inf_val=inf_val)
    results = simulated_annealing(distance_df, template_adj_mx, bay_id_list, num_buckets, iterations, temp, inf_val)
    save_results_to_csv(results, results_file)