# %%
import requests
import json
from pathlib import Path

# %%
# Part 1: get a list of routes

with open('../data/ttc-routes.json', 'r') as f:
  data = json.load(f)

routes = []
for route in data['route']:
  routes.append(int(route['tag']))

# %%
# Part 2: get the stops from each lines

for route in routes:
  # making a GET request
  response = requests.get('https://retro.umoiq.com/service/publicJSONFeed?command=routeConfig&a=ttc&r=' + str(route))
  # make sure the path exist
  path = '../data/ttc/routes'
  Path(path).mkdir(parents=True, exist_ok=True)
  # store the result into a json file.
  with open(path + '/' + str(route) + '.json', 'w') as outfile:
    print('now processing ' + str(route))
    json.dump(response.json(), outfile)


