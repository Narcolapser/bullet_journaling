import requests
import json
from flask import Flask, render_template, request, send_file
from datetime import datetime, timedelta as delta

app = Flask(__name__)

year = '2023'
season = f'Winter {year}'

# The first sunday of the quarter
sdate = datetime.strptime('2023-01-01', '%Y-%m-%d')

# The last saturday of the quarter
fdate = datetime.strptime('2023-03-25', '%Y-%m-%d')


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
    date = sdate + delta(days=dow)
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

# Quarter Pages
@app.route('/quarter_goals')
def quarter_goals():
    subtitle = 'Season of Nothing New'
    goals = [goal.replace('\n','') for goal in '''
* Clear everything off of Habitica todo list
'''.split('* ')[1:]]
    return render_template('goals.html',title=season,goals=goals,subtitle=subtitle)

@app.route('/daily_planner')
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
    activities = ['Screwtape', 'Dishes','Exercise','Update Journal']
    return render_template('daily_planner.html',season=season, months=months, days=days, activities=activities)

@app.route('/weekly_planner')
def weekly_planner():
    activities = '''
* Nothing New
* Read News Letter
* Lucy Time!
* Games with Ben
* Couples Bible study
* Chore
* House Project
* Clean Garage
* Clean Desks
* Water Plants
* Swap Batteries'''.split('* ')[1:]
    dates = get_date_sequence(SUNDAY)
    return render_template('weekly_planner.html',season=season,activities=activities,weeks=dates)

@app.route('/monthly_recap')
def monthly_recap():
    return render_template('icon_list_sections.html',title='Monthly Recap',rows = 7, img='notebook.png',height='12',
                           sections=['January','February','March'])

@app.route('/pixels')
def pixels():
    emotions = ['Happy','Productive','Fun','Relaxed','Tired','Excited','Sad','Anxious']
    dates = get_multi_date_sequence([SUNDAY,MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY])
    
    # Can't use a set because sets are unordered.
    months = []
    for date in dates:
        month = date.strftime('%B')
        if month not in months:
            months.append(month)

    # Pad the months to get calendars
    calendars = {month:[] for month in months}
    for date in dates:
        month = date.strftime('%B')
        if len(calendars[month]) == 0:
            day_of_week = int(date.strftime('%w'))
            for pad in range(day_of_week):
                calendars[month].append('')
        calendars[month].append(date.strftime('%d'))
        
    # Convert the calendars into lists of weeks for the template to render on.
    weeks = {month:[] for month in months}
    for month in calendars:
        dow = 0
        week = []
        for date in calendars[month]:
            week.append(date)
            dow += 1
            if dow == 7:
                dow = 0
                weeks[month].append(week)
                week = []
        if dow != 0:
            # If a month only has 1 week in it, we need to pad the end just to make sure the widths all line up.
            while dow < 7:
                week.append('')
                dow += 1
            weeks[month].append(week)
    
    return render_template('pixels.html',months=months,weeks=weeks,season=season,emotions=emotions)

@app.route('/celebrations')
def celebrations():
    return render_template('icon_list.html',title='Celebrations!',rows=21,img='tada.png',height='20')

@app.route('/hospitality')
def hospitality():
    return render_template('hospitality.html')

@app.route('/couples_bible_study')
def couples_bible_study():
    return render_template('weekly.html',weeks=get_date_sequence(SATURDAY), title='Couple\'s Bible Study')
    
    
@app.route('/dragon')
def dragon():
    return render_template('icon_list.html',title='The Dragon Book',rows=12,img='book.png',height='30',background='dragonbook.jpg')

@app.route('/house_projects')
def house_projects():
    return render_template('icon_list.html',title='House Projects',rows=10,img='checkedbox.png',height='60', background='handyman.png')

@app.route('/cathol')
def cc():
    return render_template('icon_list.html',title='Why We\'re Catholic',rows=25,img='book.png',height='15',background='whywerecatholic.jpeg')

@app.route('/movies')
def movies():
    return render_template('weekly.html',weeks=get_date_sequence(SUNDAY), title='Movies', background='popcorn.png')

@app.route('/lucy_time')
def lucy_time():
    return render_template('weekly.html',weeks=get_date_sequence(TUESDAY), title='Lucy Time', background='playground.png')

@app.route('/sensors')
def sensors():
    return render_template('icon_list.html',title='Sensor Projects',rows=24,img='sensor.png',height='15',background='sensor.png')
    
@app.route('/ham')
def ham():
    sections = [['Technical License',[('Questions',100),('Questions',200),('Questions',300),('Questions',400),('Questions',423)]],
     ['General License License',[('Questions',100),('Questions',200),('Questions',300),('Questions',400),('Questions',454)]]]
    return render_template('bars.html',title='HAM Radio Test Prep',sections=sections)

@app.route('/rokenbok')
def rokenbok():
    return render_template('icon_list_sections.html',title='Rokenbok Experiments',rows = 7, img='Radio Tower.png',height='12',
                           sections=['Observing','Decoding','Transmitting'])

@app.route('/run')
def run():
    dates = get_multi_date_sequence([MONDAY,THURSDAY])
    #dates = get_date_sequence(TUESDAY)
    units = ['Miles','BPM','Time']
    unit_steps = [[float(i)/10 for i in range(16,36)],range(120,200,4),range(15,35)]
    return render_template('graph.html',dates=dates,title='Running',units=units,unit_steps=unit_steps)

@app.route('/arms')
def arms():
    dates = get_date_sequence(TUESDAY)
    items = ['Chest Press','Angel','Bicep Curl','Tricep Curl','Bent Over Row']
    steps = 5
    item_bounds = [[10,45],[10,45],[10,45],[10,45],[10,45]]
    item_intervals = [int((bound[1]-bound[0])/steps) for bound in item_bounds]
    item_units = []
    for i,bounds in enumerate(item_bounds):
        units = [bounds[1]]
        for j in range(steps-1):
            units.append(bounds[1] - item_intervals[i] * (j+1))
        item_units.append(units)
    return render_template('stacked_graph.html',dates=dates,title='Weight Lifting: Arms',items=items,
        item_units=item_units, steps=steps)

@app.route('/legs')
def legs():
    dates = get_date_sequence(FRIDAY)
    items = ['Step Ups','Glute Bridge','Weighted Lounges','Goblet Squats','Farmers Carry']
    steps = 5
    item_bounds = [[10,45],[10,45],[10,30],[10,45],[70,150]]
    item_intervals = [int((bound[1]-bound[0])/steps) for bound in item_bounds]
    item_units = []
    for i,bounds in enumerate(item_bounds):
        units = [bounds[1]]
        for j in range(steps-1):
            units.append(bounds[1] - item_intervals[i] * (j+1))
        item_units.append(units)
    return render_template('stacked_graph.html',dates=dates,title='Weight Lifting: Legs',items=items,
        item_units=item_units, steps=steps)

@app.route('/notes')
def notes():
    return render_template('icon_list.html',title='Notes',rows=21,img='notebook.png',height='20')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
