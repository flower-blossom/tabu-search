### Read file
import os.path

node_data_filename = "/../data/berlin52.tsp"

with open(os.path.dirname(__file__) + node_data_filename) as f_obj:
    node_data = f_obj.readlines()

# Refining distance data
node_data = node_data[6:-2]

node_coord_dict = {}

for i in range(0, len(node_data)):
    node_coord_dict[i+1] = node_data[i][2:-1].split()

print(node_coord_dict)