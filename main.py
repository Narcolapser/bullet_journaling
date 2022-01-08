import requests
import json
from flask import Flask, render_template, request, send_file
from datetime import datetime, timedelta as delta

app = Flask(__name__)

season = "Winter 2022"

# The first sunday of the quarter
sdate = datetime.strptime('2022-01-02', '%Y-%m-%d')

# The last saturday of the quarter
fdate = datetime.strptime('2022-03-26', '%Y-%m-%d')


SUNDAY = 0
MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6

def get_multi_date_sequence(days_of_week):
    dow_list = [sdate + delta(days=dow) for dow in days_of_week]
    week_delta = delta(days=7)
    dates = []
    while dow_list[0] <= fdate:
        for i,date in enumerate(dow_list):
            dates.append(date)
            dow_list[i] = date + week_delta
    return dates

def get_date_sequence(dow):
    date = sdate + delta(days=SATURDAY)
    week_delta = delta(days=7)
    dates = []
    while date <= fdate:
        dates.append(date)
        date = date + week_delta
    return dates

@app.route('/')
def root():
    pages = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods:
            pages.append(rule.endpoint)
    return render_template('index.html',pages=pages)

@app.route('/quarter_goals')
def quarter_goals():
    subtitle = 'Season of Automation'
    goals = ['Budget Automations - Walmart', ' Budget Automations - Ace', 'Budget Automations - Amazon',
        'Budget Automations - Server for scrapers', 'Smartify all touchplate lights',
        'Get Home Assistant usable and Dependable for Megan', 'Smartify Garage Doors', 'Setup 433mhz network',
        'Thermometers in various rooms', 'Purchase and setup 3D printer', 'Read Theology Book', 'Beat Ringfit',
        'Improve bullet journal software','Re-organize desk','Fix Basement lights', 'Upgrade home WiFi', 
        'Wire new outlet for sump pump']
    return render_template('goals.html',title=season,goals=goals,subtitle=subtitle)

@app.route('/daily_planner/')
def daily_planner():
    # We later strip off the date and use just the month, so we just need to know that we got to the next month with
    # these sequence of dates not that we got to the first of said month. 
    months = [sdate+delta(days=0),sdate+delta(days=31),sdate+delta(days=62)]
    ms = '%Y-%m'
    days = []
    day = delta(days=1)
    for month in months:
        temp_month = datetime.strptime(month.strftime(ms),ms)
        dc = 0
        while temp_month.month == month.month:
            temp_month += day
            dc += 1
        days.append(dc)
    activities = ['Update Journal', 'Dishes','Exercise','Bible']
    return render_template('daily_planner.html',season=season, months=months, days=days, activities=activities)

@app.route('/weekly_planner')
def weekly_planner():
    activities = ['Chore','Clean Desk','House Project','Read News Letter','Men\'s Bible Study',
        'Couple\'s bible study','Games with Ben','Return of the thief','The Reason for God','Building Microservices',
        'Lucy Time']
    weeks = []
    dates = get_date_sequence(SUNDAY)
    return render_template('weekly_planner.html',season=season,activities=activities,weeks=dates)

@app.route('/monthly_recap')
def monthly_recap():
    return render_template('icon_list_sections.html',title='Monthly Recap',rows = 7, img='notebook.png',height='12',
                           sections=['January','February','March'])

@app.route('/hospitality')
def hospitality():
    return render_template('hospitality.html')

@app.route('/couples_bible_study')
def couples_bible_study():
    return render_template('weekly.html',weeks=get_date_sequence(SATURDAY), title='Couple\'s Bible Study')

@app.route('/movies')
def movies():
    return render_template('weekly.html',weeks=get_date_sequence(SUNDAY), title='Movies')

@app.route('/house_projects')
def house_projects():
    return render_template('weekly.html',weeks=get_date_sequence(SATURDAY), title='House Projects')

@app.route('/reasonforgod')
def reading1():
    return render_template('icon_list.html',title='Return of the Thief:</br>The Book of Pheris, Vol II',rows=14,img='book.png',height='25',background='return of the thief.jpeg')

@app.route('/queensthief')
def reading2():
    return render_template('icon_list.html',title='The Reason For God',rows=14,img='book.png',height='25',background='reason_for_God.jpg')
    
@app.route('/microservices')
def reading3():
    return render_template('icon_list.html',title='Building Microservices',rows=16,img='book.png',height='23',background='building_microservices.jpg')

@app.route('/misc_goals')
def misc_goals():
    return render_template('misc_goals.html')

@app.route('/ringfit')
def ringfit():
    dates = get_multi_date_sequence([3,5])
    units = ['BPM','Time','Calories']
    unit_steps = [range(70,150,4),range(5,25),range(20,80,3)]
    return render_template('graph.html',dates=dates,title='Ring Fit',units=units,unit_steps=unit_steps)

@app.route('/arms')
def arms():
    #dates = get_multi_date_sequence([3,5])
    dates = get_date_sequence(TUESDAY)
    units = ['Press','Angel','Curl','Tricep','Row']
    unit_steps = [range(11,31),range(11,31),range(11,31),range(11,31),range(11,31)]
    return render_template('graph.html',dates=dates,title='Weight Lifting: Arms',units=units,unit_steps=unit_steps)

@app.route('/legs')
def legs():
    #dates = get_multi_date_sequence([3,5])
    dates = get_date_sequence(THURSDAY)
    units = ['Glute','Goblet','Carry','Lift','Crunch']
    unit_steps = [range(11,31),range(11,31),range(31,91),range(11,31),range(11,31)]
    return render_template('graph.html',dates=dates,title='Weight Lifting: Legs',units=units,unit_steps=unit_steps)

@app.route('/notes')
def notes():
    return render_template('icon_list.html',title='Notes',rows=21,img='notebook.png',height='20')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
