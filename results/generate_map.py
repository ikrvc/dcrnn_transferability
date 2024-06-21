import folium
import pandas as pd
import pickle

# Function to read IDs from file and convert to numpy array
def read_ids_to_array(file_path):
    with open(file_path, 'r') as file:
        # Read the single line containing the IDs
        content = file.read()

        # Remove any trailing newline characters and split by comma
        id_list = content.strip().split(',')

        # Convert list of strings to integer if IDs are expected to be integers
        id_list = [int(id) for id in id_list]

    return id_list

def add_line(map_obj, loc1, loc2, weight, color):
    line = folium.PolyLine(locations=[loc1, loc2], weight=weight, color=color)
    map_obj.add_child(line)

def add_edges(map_obj, sensor_locations, adj_mx_filename, sensor_subset=None):
    if sensor_subset is None:
        sensor_subset = []
    with open(adj_mx_filename, "rb") as f:
        sensor_ids, sensor_id_to_ind, adj_mx = pickle.load(f)
    print(sensor_subset)
    id_to_location = {str(int(row['sensor_id'])): (row['latitude'], row['longitude']) for idx, row in sensor_locations.iterrows()}
    for i, id1 in enumerate(sensor_ids):
        for j, id2 in enumerate(sensor_ids):
            if i != j and adj_mx[i, j] > 0:
                if id1 in id_to_location and id2 in id_to_location:
                    location1 = id_to_location[id1]
                    location2 = id_to_location[id2]
                    weight = adj_mx[i, j]
                    # Create a feature group for each line to attach a popup
                    line_group = folium.FeatureGroup()
                    if int(id1) in sensor_subset and int(id2) in sensor_subset:
                        line = folium.PolyLine(locations=[location1, location2], weight=weight * 5, color='green')
                    else:
                        # line = folium.PolyLine(locations=[location1, location2], weight=weight * 5, color='red')
                        line = folium.PolyLine(locations=[location1, location2], weight=weight * 0, color='red')
                    popup_text = f"From: Sensor {id1} to Sensor {id2}, Weight: {weight:.2f}"
                    popup = folium.Popup(popup_text, parse_html=True)
                    line.add_child(popup)
                    line_group.add_child(line)
                    map_obj.add_child(line_group)

def addNodes(la_map, sensor_locations, sensor_ids=None):
    # Add points for each sensor
    for idx, row in sensor_locations.iterrows():
        if (int(row['sensor_id']) not in sensor_ids):
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,  # Set the size of the marker
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.6,
                popup=f"Sensor ID: {int(row['sensor_id'])}"  # Popup text
            ).add_to(la_map)
        else:
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,  # Set the size of the marker
                color='orange',
                fill=True,
                fill_color='orange',
                fill_opacity=0.6,
                popup=f"Sensor ID: {int(row['sensor_id'])}"  # Popup text
            ).add_to(la_map)


if __name__ == '__main__':

    sensor_locations = pd.read_csv("data/sensor_graph/graph_sensor_locations.csv")
    sensor_locations_bay = pd.read_csv("data/sensor_graph/graph_sensor_locations_bay.csv")
    # sensor_ids = read_ids_to_array("data/sensor_graph/graph_sensor_ids_subset.txt")
    # sensor_ids = [717447,716949,764101,717445,716331,717490,718045,769402,769418,764766,760987,769345,769806,717610,717456,716328,716337,769373,764853,717472,717446,773869,717492,774204,717481,769388,717465,764106,717461,717459,717571,717462,717495,769403,765604,717491,717483,717493,717497,769430,772669,717488,717463,768469,769346,760024,769405,717513,768066,717450]
    sensor_ids = [717587,717590,718072,717592,773975,773974,767454,767455,773996,773995]
    # sensor_ids = [int(i) for i in sensor_ids]
    # sensor_ids_bay = read_ids_to_array("data/sensor_graph/found_best_ids_next.txt")
    sensor_ids_bay = [404522,402359,402289,409529,400122,400213,400147,400449,401489,400717]
    la_map = folium.Map(location=[35.5522, -120.5437], zoom_start=7)
    # la_map = folium.Map(zoom_start=10)

    addNodes(la_map, sensor_locations, sensor_ids)
    addNodes(la_map, sensor_locations_bay, sensor_ids_bay)

    # IF YOU WANT TO ADD EDGES FROM ADJ_MATRIX - uncomment
    # add_edges(la_map, sensor_locations_bay, 'data/sensor_graph/adj_mx_bay.pkl', sensor_ids_bay)
    # add_edges(la_map, sensor_locations, "data/sensor_graph/adj_mx.pkl", sensor_ids)

    # Display the map
    la_map.save('LA_AND_BAY_traffic_sensors_xturn.html')
