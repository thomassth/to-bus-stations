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
    with open('../data/ttc/' + str(route) + '.json', 'r') as f:
        data = json.load(f)

    stops = []
    for stop in data['route']['stop']:
        stopTag = stop['tag']
        stops.append(stopTag)
        if stopTag in route_dictionary:
            route_dictionary[stopTag]['lines'].append(route)
        else:
            route_dictionary[stopTag] = {'lon': stop['lon'], 'lat': stop['lat'], 'title': stop['title'], 'lines':[route]}

route_array = [value for key, value in route_dictionary.items()]

with open(data_path + 'stops.json', 'w') as json_file:
    json.dump(route_array, json_file)


