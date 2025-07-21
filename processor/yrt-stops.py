# %%
import json

# %%
# Part 1: get a list of routes

with open('../data/yrt-routes.json', 'r') as f:
  data = json.load(f)

routes_set = data['result']['lines']


# %%
# Part 2: group all stop info together

stop_dictionary = {}

data_path = '../data/yrt/'

for route in routes_set:
    line_number=route['lineAbbr'].replace("|", "_")
    line_dir_dictionary = {}
    for direction in route['directions']:
        line_dir_dictionary[direction['lineDirIdContext'][0]['lineDirId']] = direction

    with open('../data/yrt/routes/' + str(line_number) + '.json', 'r') as f:
        data = json.load(f)

    for direction in data['result']['directions']:
        direction_data = line_dir_dictionary[direction['lineDirId']]
        direction_text = direction_data['directionName']
        line = direction_data['lineDirIdContext'][0]['lineAbbr']

        # print(direction_data)
        # print(direction['stops'])

        for stop in direction['stops']:
            # stopId = URL
            # stopPublicId = what you can see on bus stops

            stopPublicId = stop['stopPublicId']

            if stopPublicId in stop_dictionary:
                stop_dictionary[stop['stopPublicId']]['lines'].append(line)
                stop_dictionary[stop['stopPublicId']]['directionPerLine'].append(direction_text)

            else:
                stop_dictionary[stop['stopPublicId']] = stop
                stop_dictionary[stop['stopPublicId']]['lines'] = [line]
                stop_dictionary[stop['stopPublicId']]['directionPerLine'] = [direction_text]
        
route_array = [{**value, 'id': value['stopPublicId']} for key, value in stop_dictionary.items()]

# %%
# # Part 3: generate files

import csv

with open(data_path + 'stops.json', 'w') as json_file:
    json.dump(route_array, json_file)

with open(data_path + 'stops.csv', 'w', newline='') as csv_file:
    if route_array:
        writer = csv.DictWriter(csv_file, fieldnames=route_array[0].keys())
        writer.writeheader()
        writer.writerows(route_array)



