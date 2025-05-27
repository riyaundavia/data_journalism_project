import csv
import json

input_path = "children_lbl_cleansed.csv"
output_path = "blood_lead_by_borough.json"

formatted_data = {}

with open(input_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        borough = row["geo_area_name"]
        year = int(row["time_period"])
        
        number = int(row["Children under 6 years with elevated blood lead levels (BLL) Number BLL >=5 碌g/dL"])
        rate10 = float(row["Children under 6 years with elevated blood lead levels (BLL) Rate BLL>=10 碌g/dL per 1,000 tested"])
        rate15_note = row["Children under 6 years with elevated blood lead levels (BLL) Rate BLL>=15 碌g/dL per 1,000 tested_NOTES"]
        
        if borough not in formatted_data:
            formatted_data[borough] = {}
        
        formatted_data[borough][year] = {
            "number_BLL_5": number,
            "rate_BLL_10": rate10,
            "note_BLL_15": rate15_note.strip() if rate15_note else None
        }

with open(output_path, "w") as jsonfile:
    json.dump(formatted_data, jsonfile, indent=2)
