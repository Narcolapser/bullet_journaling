import requests
import json
from flask import Flask, render_template, request
from datetime import datetime, timedelta as delta

app = Flask(__name__)

@app.route('/')
def root():
    pages = []
    return render_template('index.html',pages=pages)

@app.route('/weekly/<start>/<weeks>')
def weekly(start, weeks):
    date = datetime.strptime(start, '%Y-%m-%d')
    dates = []
    week_delta = delta(days=7)
    weeks = int(weeks)
    print(f'Starting with {date} for {weeks} weeks')
    for week in range(weeks):
        dates.append(date)
        print(date.strftime('%m-%d'))
        date = date + week_delta
    return render_template('weekly.html',weeks=dates)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
