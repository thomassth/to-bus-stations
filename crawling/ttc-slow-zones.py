# %%
import requests
import json
from pathlib import Path

# %%
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64); to-bus-stations'}
response = requests.get('https://www.ttc.ca/riding-the-ttc/Updates/Reduced-Speed-Zones', headers=headers)
# make sure the path exist
path = '../data/ttc'
Path(path).mkdir(parents=True, exist_ok=True)
print(response)
# store the result into a json file.
with open(path + '/ttc-slow-zones.html', 'w',  encoding='utf-8') as outfile:
    outfile.write(response.text)



