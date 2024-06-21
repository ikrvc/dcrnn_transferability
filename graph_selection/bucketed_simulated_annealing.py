import time

from lib.utils import load_graph_data
from simulated_annealing import neighbor
from distance_functions import dist
from simulated_annealing_helper_functions import *

adj_mx = '../data/sensor_graph/adj_mx_50subset.pkl'
results_file = '../results/simulated_annealing_results_big_abssum0.csv'
num_buckets = 50
num_selected = 50
min_distance = 8000000
max_distance = 16000000
temp = 10000
inf_val = 0
dist_mode = 'fro'

def get_bucket_targets(min_distance, max_distance, num_buckets=100):
    """Generate target distances for each bucket."""
    numbers = np.linspace(min_distance, max_distance, num_buckets+1)
    return zip(numbers, numbers[1:])

def simulated_annealing_for_buckets(distance_df, template_matrix, total_sensor_ids, num_buckets=100, num_selected=50, temp=100, inf_val=40000):
    targets = get_bucket_targets(min_distance, max_distance, num_buckets)
    results = []
    for target_min, target_max in targets:
        print(target_min, " ", target_max)
        start = time.time()
        # You can modify this to aim for a specific target range
        best_cost, best_sensors = simulated_annealing(distance_df, template_matrix, total_sensor_ids, target_min, target_max, num_selected=num_selected, temp=temp, inf_val=inf_val)
        results.append((best_cost, best_sensors))
        end = time.time()
        print("Graph finished in ", end-start, " seconds")
        print(best_cost)
    return results


def target_cost_function(cost, target_min, target_max):
    """ Custom cost function to penalize deviations from the target range. """
    if cost < target_min:
        return abs(cost - target_min)/1000
    elif cost > target_max:
        return abs(cost - target_max)/1000
    return 0


def simulated_annealing(distances, template_matrix, total_sensor_ids, target_min, target_max, num_selected=50,
                        iterations=10000, temp=100, cooling_rate=0.95, inf_val=40000):
    best_cost = float('inf')
    best_adjusted_cost = float('inf')
    best_ids = None

    current_solution = initialize_sensors(total_sensor_ids, num_selected)
    current_adj_matrix = get_adjacency_matrix(distances, current_solution, inf_val=inf_val)
    current_cost = dist(current_adj_matrix, template_matrix, dist_mode)

    adjusted_current_cost = target_cost_function(current_cost, target_min, target_max)
    for i in range(iterations):
        new_solution = neighbor(current_solution, total_sensor_ids)
        new_adj_matrix = get_adjacency_matrix(distances, new_solution, inf_val=inf_val)
        new_cost = dist(new_adj_matrix, template_matrix, dist_mode)
        adjusted_cost = target_cost_function(new_cost, target_min, target_max)
        if adjusted_cost < adjusted_current_cost or np.random.rand() < np.exp((adjusted_current_cost-adjusted_cost) / temp):
            current_solution = new_solution
            adjusted_current_cost = adjusted_cost
            if adjusted_cost < best_adjusted_cost:
                best_cost = new_cost
                best_adjusted_cost = adjusted_cost
                best_ids = new_solution
        temp *= cooling_rate
        if adjusted_cost == 0:
            break
    return best_cost, best_ids

if __name__ == '__main__':
    template_sensor_ids, template_sensor_id_to_ind, _ = load_graph_data(
        adj_mx)
    distance_df = pd.read_csv('../data/sensor_graph/distances_bay_2017.csv', dtype={'from': 'str', 'to': 'str'})
    distance_df_la = pd.read_csv('../data/sensor_graph/distances_la_2012.csv', dtype={'from': 'str', 'to': 'str'})
    bay_id_list = read_ids_to_array("../data/sensor_graph/graph_sensor_ids_bay.txt")
    la_id_list = read_ids_to_array("../data/sensor_graph/graph_sensor_ids.txt")
    template_adj_mx = get_adjacency_matrix(distance_df_la, template_sensor_ids, inf_val=inf_val)
    results = simulated_annealing_for_buckets(distance_df, template_adj_mx, bay_id_list, num_buckets, num_selected=num_selected, temp=temp, inf_val=inf_val)
    save_results_to_csv(results, results_file)