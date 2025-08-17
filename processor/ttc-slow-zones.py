# %%
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pathlib import Path

# %%
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64); to-bus-stations'}


with open('../data/ttc/ttc-slow-zones.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup_html = BeautifulSoup(html, 'html.parser')


# %% [markdown]
# ## save rendered slow zone img

# %%
slow_zone_img = ''

imgs = soup_html.select('img')

for img in imgs:
    if('reduced speed zone' in str(img.get('alt')).lower()):
        slow_zone_img = str(img.get('src'))

if(slow_zone_img):
    response = requests.get(slow_zone_img, headers=headers)

    # make sure the path exist
    path = '../data/ttc/slow-zone'
    Path(path).mkdir(parents=True, exist_ok=True)

    with open(path + '/slow-zone.svg', 'w', encoding='utf-8') as f:
        f.write(response.text)

# %% [markdown]
# ## save slow zone table data

# %%
table_headers = soup_html.select('h2')

slow_zone_table_names = [header.get_text() for header in table_headers]

tables = soup_html.select('table')

slow_zone_table = []

table_header = []

for row_index,table in enumerate(tables):
    table_name = slow_zone_table_names[row_index]

    rows = []
    for row in (table.find_all('tr')):
        cols = row.find_all(['td', 'th'])
        row_data = [col.get_text(strip=True) for col in cols]
        row_data.insert(0, table_name)
        rows.append(row_data)
    
    table_header=rows[0]
    df = pd.DataFrame(rows[1:])
    slow_zone_table.append(df)

# change the 1st col of the merged table title

table_header[0] = 'Line'

slow_zone_table.insert(0, pd.DataFrame([table_header]))

# Merge all tables (you can customize how)
merged = pd.concat(slow_zone_table, ignore_index=True)

# make sure the path exist
path = '../data/ttc/slow-zone/'
Path(path).mkdir(parents=True, exist_ok=True)

# Save to CSV
merged.to_csv(path + 'ttc-slow-zones.csv', index=False, header=False)



