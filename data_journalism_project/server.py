from flask import Flask, redirect
from flask import render_template
from flask import request
import json

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return redirect('/about')

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)