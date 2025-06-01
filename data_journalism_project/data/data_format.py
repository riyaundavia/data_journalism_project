import csv
import json
formatted_data = {}

with open("data/children_elevated_bll_cleansed.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        borough = row["geo_area_name"]
        year = int(row["time_period"])
        number = int(row["Children under 6 years with elevated blood lead levels (BLL) Number BLL >=5 碌g/dL"])
        
        if borough not in formatted_data:
            formatted_data[borough] = {}
        
        formatted_data[borough][year] = {
            "numberBll5": number
        }

with open("blood_lead_levels_by_borough.json", "w") as jsonfile:
    json.dump(formatted_data, jsonfile, indent=2)

print("JSON saved to blood_lead_levels_by_borough.json")
