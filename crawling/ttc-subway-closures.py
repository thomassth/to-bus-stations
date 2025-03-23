# %%
import json
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path

# %%
# Part 1: retrieve the HTML from the JSON response
with open('../data/ttc-subway-closures.json') as f:
    data = json.load(f)

results = data['Results']

html_parts = list(map(lambda x: x['Html'], results))

# %%
# Part 2: data cleanup
def clean_text(text):
    return text.replace('\xa0', ' ').replace('â€“', '-').replace('\u2013', '-').strip()

def parse_date(date_str):
    return datetime.strptime(date_str, '%B %d, %Y').date().isoformat()

closures = [
    {
        'start_date': parse_date(clean_text((soup := BeautifulSoup(html, 'html.parser')).select_one('.field-starteffectivedate').get_text())),
        'end_date': parse_date(clean_text(soup.select_one('.field-endeffectivedate').get_text())),
        'line': clean_text(soup.select_one('.field-routename').get_text()),        
        'text': clean_text(soup.get_text()),

    }
    for html in html_parts
]



# %%
# Part 3: save the data

# make sure the path exist
path = '../data/ttc/subway-closures'
Path(path).mkdir(parents=True, exist_ok=True)

# Save each object to a separate JSON file
for closure in closures:
    filename = f"{closure['start_date']}-{closure['line'].split()[1]}.json"
    filepath = Path(path) / filename
    with open(filepath, 'w') as outfile:
        print('now processing ' + str(filename))
        json.dump(closure, outfile)

print('done')


