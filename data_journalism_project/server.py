from flask import Flask, redirect
from flask import render_template
from flask import request
import json
import os
json_path = os.path.join(os.path.dirname(__file__), 'data', 'data.json')

with open(json_path) as f:
    all_bll_data = json.load(f)

all_values = [
    year_data['numberBll5']
    for borough_data in all_bll_data.values()
    for year_data in borough_data.values()
]

average_bll = round(sum(all_values) / len(all_values))

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return redirect('/about')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/macro')
def macro():
    with open(json_path) as f:
        data = json.load(f)

    years = sorted(map(int, next(iter(data.values())).keys()))

    def make_endpoints(values):
        return [(values[i], values[i+1]) for i in range(len(values)-1)]

    borough_endpoints = {}
    for borough, year_dict in data.items():
        sorted_vals = [year_dict[str(y)]['numberBll5'] for y in years]
        borough_endpoints[borough] = make_endpoints(sorted_vals)

    all_vals = [v['numberBll5'] for d in data.values() for v in d.values()]
    y_max = max(all_vals)
    y_min = 0

    return render_template(
        "macro.html",
        average_bll=average_bll,
        years=years,
        borough_endpoints=borough_endpoints,
        y_max=y_max,
        y_min=y_min
    )

@app.route('/micro')
def micro():
    year = request.args.get('year', '2010')
    with open(json_path) as f:
        data = json.load(f)

    # Extract values for the selected year only
    values = {
        borough: data[borough][year]['numberBll5']
        for borough in data if year in data[borough]
    }

    min_val = min(values.values())
    max_val = max(values.values())

    # Scale lightness between 35% (dark red) to 85% (light pink)
    def scale_lightness(val):
        if max_val == min_val:
            return 60  # default mid-lightness
        norm = (val - min_val) / (max_val - min_val)
        return round(85 - 50 * norm, 1)  # inverse because lighter = lower numbers

    borough_lightness = {borough: scale_lightness(val) for borough, val in values.items()}

    # Also create legend values
    legend_values = [min_val + i * (max_val - min_val) / 9 for i in range(10)]

    return render_template(
        'micro.html',  # use your actual filename
        year=year,
        average_bll=average_bll,
        borough_lightness=borough_lightness,
        legend_values=legend_values,
        borough_data=values
    )

if __name__ == '__main__':
    app.run(debug=True)