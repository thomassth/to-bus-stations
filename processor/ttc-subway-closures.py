# %%
import json

# Part 1: retrieve the HTML from the JSON response
with open('../data/ttc-subway-closures.json') as f:
    data = json.load(f)

results = data['Results']

html_parts = (x['Html'] for x in results)

# %%
from bs4 import BeautifulSoup
from datetime import datetime

# Part 2: data cleanup
def clean_text(text):
    return text.replace('\xa0', ' ').replace('â€“', '-').replace('\u2013', '-').strip()

def convert_date_string(input_date_string):
    return datetime.strptime(input_date_string, '%B %d, %Y').date().isoformat()

today_date = datetime.now().date().isoformat()

closures = []
for i, html in enumerate(html_parts):
    soup = BeautifulSoup(html, 'html.parser')
    effective_date_elem = soup.select_one('.sa-effective-date').get_text()
    line_text = soup.select_one('.field-routename').get_text()
    desc_text = soup.select_one('.field-satitle').get_text()


    start_date = ''
    end_date = ''
    if "to" in effective_date_elem:
        start_date, end_date = [d.strip() for d in effective_date_elem.split("to", 1)]
    else:
        start_date = effective_date_elem
        end_date = effective_date_elem

    if start_date and end_date and line_text and desc_text:
        url = results[i].get('Url', '')
        closures.append({
            'start_date': convert_date_string(clean_text(start_date)),
            'end_date': convert_date_string(clean_text(end_date)),
            'line': clean_text(line_text),
            'text': clean_text(desc_text),
            'url': f"https://www.ttc.ca{url}" if url.startswith('/') else "https://www.ttc.ca",
            'last_shown': today_date
        })

# %%
from datetime import timedelta
from pathlib import Path

# Part 3: save the data

def get_date(input_date_string):
    return datetime.strptime(input_date_string, '%Y-%m-%d').date()

# make sure the path exist
path = '../data/ttc/subway-closures'
Path(path).mkdir(parents=True, exist_ok=True)

# Create a dictionary to hold closures by date
# Dates without closures will be added as empty lists
closures_by_date = {}
all_dates = [date for closure in closures for date in (get_date(closure['start_date']), get_date(closure['end_date']))]
earliest_date = min(all_dates)
latest_date = max(all_dates)
print(f"Earliest date: {earliest_date.isoformat()}, Latest date: {latest_date.isoformat()}")

current_date = earliest_date

while current_date <= latest_date:
    date_str = current_date.isoformat()
    closures_by_date[date_str] = []
    current_date += timedelta(days=1)  # Increment by one day


for closure in closures:
    start_date = closure['start_date']
    end_date = closure['end_date']
    
    # Add closure to dates between start_date and end_date
    current_date = get_date(start_date)
    end_date_obj = get_date(end_date)
    while current_date <= end_date_obj:
        date_str = current_date.isoformat()
        if date_str not in closures_by_date:
            closures_by_date[date_str] = []
        closures_by_date[date_str].append(closure)
        current_date += timedelta(days=1)

with open(Path(path) / "lastupdated", "w") as file:
    file.write(str(today_date))


# Save each object to a separate JSON file
for date, closures in closures_by_date.items():
    filename = f"{date}.json"
    filepath = Path(path) / filename
    if filepath.exists():
        with open(filepath, 'r') as infile:
            existing_closures = json.load(infile)
            # Combine both lists, prioritizing new closures
            combined = existing_closures + closures

            # Use a dict to deduplicate by 'url', new closures overwrite old ones
            merged = {closure['url']: closure for closure in combined}

            # Resulting list of unique closures
            closures = list(merged.values())
    with open(filepath, 'w') as outfile:
        print(f'now processing {filename}')
        json.dump(closures, outfile)

print(f'Done! Processed {len(closures_by_date)} files, from {earliest_date.isoformat()} to {latest_date.isoformat()}')



