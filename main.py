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

@app.route('/daily_planner/')
def daily_planner():
    season = "Spring 2021"
    ms = '%Y-%m'
    months = [datetime.strptime('2021-04', ms),datetime.strptime('2021-05', ms), datetime.strptime('2021-06', ms)]
    days = []
    day = delta(days=1)
    for month in months:
        temp_month = datetime.strptime(month.strftime(ms),ms)
        dc = 0
        while temp_month.month == month.month:
            temp_month += day
            dc += 1
        days.append(dc)
    activities = ['Spanish','Dishes','Exercise']
    return render_template('daily_planner.html',season=season, months=months, days=days, activities=activities)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
