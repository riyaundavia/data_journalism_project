from flask import Flask, redirect
from flask import render_template
from flask import request
import json
import os
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'blood_lead_levels_by_borough.json')

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return redirect('/about')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/macro')
def macro():
    with open(DATA_PATH) as f:
        data = json.load(f)

    # Build a list of years
    years = list(next(iter(data.values())).keys())
    years = sorted(map(int, years))

    return render_template("macro.html", data=data, years=years)

import os

@app.route('/micro')
def micro():
    year = request.args.get("year", type=int)
    if not year:
        return "Missing year", 400

    # Use path relative to this file's location
    json_path = os.path.join(os.path.dirname(__file__), "data", "blood_lead_levels_by_borough.json")
    with open(json_path) as f:
        full_data = json.load(f)

    year_data = {}
    for borough, yearly in full_data.items():
        if str(year) in yearly:
            year_data[borough] = yearly[str(year)]["numberBll5"]

    values = list(year_data.values())
    min_val = min(values)
    max_val = max(values)

    def compute_lightness(val):
        percent = (val - min_val) / (max_val - min_val) if max_val != min_val else 0
        return round(85 - percent * 55)

    borough_lightness = {
        "Bronx": compute_lightness(year_data.get("Bronx", min_val)),
        "Brooklyn": compute_lightness(year_data.get("Brooklyn", min_val)),
        "Manhattan": compute_lightness(year_data.get("Manhattan", min_val)),
        "Queens": compute_lightness(year_data.get("Queens", min_val)),
        "Staten Island": compute_lightness(year_data.get("Staten Island", min_val))
    }

    legend_values = [round(min_val + (max_val - min_val) / 9 * i) for i in range(10)]

    return render_template(
        "micro.html",
        year=year,
        borough_lightness=borough_lightness,
        legend_values=legend_values
    )

if __name__ == '__main__':
    app.run(debug=True)