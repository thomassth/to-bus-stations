# %%
import json

# Part 1: retrieve the HTML from the JSON response
with open('../data/ttc-subway-closures.json') as f:
    data = json.load(f)

results = data['Results']

html_parts = list(map(lambda x: x['Html'], results))

# %%
from bs4 import BeautifulSoup
from datetime import datetime

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
        'url': f"https://www.ttc.ca{results[i]['Url']}"

    }
    for i, html in enumerate(html_parts)
]

# %%
from datetime import timedelta
from pathlib import Path

# Part 3: save the data

# make sure the path exist
path = '../data/ttc/subway-closures'
Path(path).mkdir(parents=True, exist_ok=True)

# sort by start_date
closures_by_date = {}
for closure in closures:
    start_date = closure['start_date']
    end_date = closure['end_date']
    
    # Add closure to dates between start_date and end_date
    current_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
    while current_date <= end_date_obj:
        date_str = current_date.isoformat()
        if date_str not in closures_by_date:
            closures_by_date[date_str] = []
        closures_by_date[date_str].append(closure)
        current_date += timedelta(days=1)

# Save each object to a separate JSON file
for date, closures in closures_by_date.items():
    filename = f"{date}.json"
    filepath = Path(path) / filename
    with open(filepath, 'w') as outfile:
        print('now processing ' + str(filename))
        json.dump(closures, outfile)

print('done')


