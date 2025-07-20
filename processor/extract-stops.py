# %%
import json

# %%
# Part 1: get a list of routes

with open('../data/ttc-routes.json', 'r') as f:
  data = json.load(f)

routes = []
for route in data['route']:
  routes.append(int(route['tag']))

# %%
# Part 2: group all stop info together

route_dictionary = {}

data_path = '../data/ttc/'

for route in routes:
    with open('../data/ttc/routes/' + str(route) + '.json', 'r') as f:
        data = json.load(f)

    for direction in data['route']['direction']:
        directionText = direction['title'].split(" - ")[0]
        for stop in direction['stop']:
            tag = stop['tag']
            if 'branch' in direction:
                if tag in route_dictionary:
                    route_dictionary[tag]['lines'].append(direction['branch'])
                    if directionText not in route_dictionary[tag]['directions']:
                        route_dictionary[tag]['directions'] = ", ".join([route_dictionary[tag]['directions'], directionText])
                else:
                    filteredStop = [item for item in data['route']['stop'] if item['tag'] == tag]
                    route_dictionary[tag] = filteredStop[0]
                    route_dictionary[tag]['directions'] = directionText
                    route_dictionary[tag]['lines'] = [direction['branch']]

filtered_dict = {key: value for key, value in route_dictionary.items() if 'stopId' in value}
route_array = [{**value, 'id': value['stopId']} for key, value in filtered_dict.items()]

# %%
# Part 3: generate files

import csv

with open(data_path + 'stops.json', 'w') as json_file:
    json.dump(route_array, json_file)

with open(data_path + 'stops.csv', 'w', newline='') as csv_file:
    if route_array:
        writer = csv.DictWriter(csv_file, fieldnames=route_array[0].keys())
        writer.writeheader()
        writer.writerows(route_array)



