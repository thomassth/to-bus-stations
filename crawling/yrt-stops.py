# %%
import requests
import json
from pathlib import Path

# %%
# Part 1: get a list of routes

with open('../data/yrt-routes.json', 'r') as f:
  data = json.load(f)

routesData = data['result']['lines']


# %%
# Part 2: get the stops from each lines

for route in routesData:
  line_number=route['lineAbbr'].replace("|", "_")
  print('now processing ' + str(line_number))  
  # making a POST request
  data = {
    "version":"1.1","method":"GetLineDetails","params":{"lineId":route['lineIdContexts'][0]['lineId']}
  }
  response = requests.post('https://tripplanner.yrt.ca/TI_FixedRoute_Line', json=data)
  # make sure the path exist
  path = '../data/yrt/routes'
  Path(path).mkdir(parents=True, exist_ok=True)
  # store the result into a json file.
  with open(path + '/' + str(line_number) + '.json', 'w') as outfile:
    json.dump(response.json(), outfile)


