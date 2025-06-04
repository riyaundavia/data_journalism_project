import json

formatted_data = {}

with open("data/data_cleansed.csv", encoding='utf-8') as csvfile:
    lines = csvfile.readlines()

headers = lines[0].strip().split(',')
geo = headers.index("geo_area_name")
years = headers.index("time_period")
bll = None

for i, header in enumerate(headers):
    if "BLL" in header:
        bll = i
        break  # Stop at the first match

if bll is None:
    raise ValueError("No header containing 'BLL' was found.")

for line in lines[1:]:
    cols = line.strip().split(',')
    
    borough = cols[geo]
    year = int(cols[years])
    
    try:
        number = int(cols[bll])
    except ValueError:
        continue

    if borough not in formatted_data:
        formatted_data[borough] = {}

    formatted_data[borough][year] = {
        "numberBll5": number
    }

# JSON
with open("data.json", "w") as jsonfile:
    json.dump(formatted_data, jsonfile, indent=2)
