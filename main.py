import requests
import json
from flask import Flask, render_template, request, send_file
from datetime import datetime, timedelta as delta

app = Flask(__name__)

year = '2024'
season = f'Winter {year}'

# The first sunday of the quarter
sdate = datetime.strptime('2024-01-07', '%Y-%m-%d')

# The last saturday of the quarter
fdate = datetime.strptime('2024-03-30', '%Y-%m-%d')


SUNDAY = 0
MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6
FULL_WEEK = [SUNDAY,MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY]


def get_specific_multi_date_sequence(days_of_week,start,end):
    dow_list = [start + delta(days=dow) for dow in days_of_week]
    week_delta = delta(days=7)
    dates = []
    while dow_list[0] <= end:
        for i,date in enumerate(dow_list):
            if date > end:
                break
            dates.append(date)
            dow_list[i] = date + week_delta
    return dates

def get_multi_date_sequence(days_of_week):
    return get_specific_multi_date_sequence(days_of_week,sdate,fdate)

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
            if rule.endpoint in ['root','static']:
                continue
            pages.append(rule.endpoint)
    pages.sort()
    return render_template('index.html',pages=pages)


# Annual pages
@app.route('/title_page')
def title_page():
    return render_template('cover.html')

@app.route('/annual_goals')
def annual_goals():
    goals = [goal.replace('\n','') for goal in '''
* Learn UT5
* Make a game for switch
* Read a CS book each quarter
* Participate in NaNoWriMo
* Participate in Advent of Code
* Spend more time outside
* Slow down an enjoy things more
* Get promoted to Dev III
* Learn to use my sextant
'''.split('* ')[1:]]
    return render_template('goals.html',title='Annual Goals',goals=goals,subtitle='')

@app.route('/themes_page')
def themes_page():
    return render_template('icon_list.html',title='Themes',rows=4,img='rainbow.png',height='150')

@app.route('/body')
def body():
    months = ['April','May','June','July','August','September','October','November','December','January','February','March']
    return render_template('body_fat.html',year=year,months=months)

@app.route('/new_games')
def new_games():
    return render_template('icon_list.html',title='Games (Video and Board)',rows=12,img='d20.png',height='40')
    
@app.route('/books')
def books():
    return render_template('icon_list.html',title='Books',rows=25,img='d20.png',height='12')

@app.route('/events')
def events():
    return render_template('icon_list.html',title='Notable Events',rows=12,img='calendar.jpg',height='40')

@app.route('/annual_pixels')
def annual_pixels():
    emotions = ['Happy','Fun','Relaxed','Productive','Tired','Sad','Anxious']
    sdate1 = datetime.strptime('2023-04-01', '%Y-%m-%d')
    sdate2 = datetime.strptime('2023-08-01', '%Y-%m-%d')
    sdate3 = datetime.strptime('2023-12-01', '%Y-%m-%d')

    fdate1 = datetime.strptime('2023-07-31', '%Y-%m-%d')
    fdate2 = datetime.strptime('2023-11-30', '%Y-%m-%d')
    fdate3 = datetime.strptime('2024-03-31', '%Y-%m-%d')
    
    col1 = get_specific_multi_date_sequence(FULL_WEEK, sdate1, fdate1)
    col2 = get_specific_multi_date_sequence(FULL_WEEK, sdate2, fdate2)
    col3 = get_specific_multi_date_sequence(FULL_WEEK, sdate3, fdate3)
    cols = [col1, col2, col3]
    
    collections = []
    
    for col in cols:
        # Can't use a set because sets are unordered.
        months = []
        for date in col:
            month = date.strftime('%B')
            if month not in months:
                months.append(month)
            if len(months) == 4:
                break

        # Pad the months to get calendars
        calendars = {month:[] for month in months}
        for date in col:
            month = date.strftime('%B')
            if month not in calendars:
                break

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
        
        collections.append({'months':months,'weeks':weeks})
    return render_template('pixels_annual.html',collections=collections,emotions=emotions)


# Quarter Pages - Recurring
@app.route('/quarter_goals')
def quarter_goals():
    subtitle = 'Season of Exodus'
    goals = [goal.replace('\n','') for goal in '''
* Learn to use my Sextant
* Winter Camp
* Organize Bulk Spice Storage
* Develop Compost Plan
* Develop Garden Plan for next year
* Design a processor in Cedar Logic
* Flash Dreame to custom firmware
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
    print(months)
    for month in months:
        temp_month = datetime.strptime(month.strftime(ms),ms)
        dc = 0
        while temp_month.month == month.month:
            temp_month += day
            dc += 1
        days.append(dc)
    activities = ['Exodus', 'Dishes','Exercise','Update Journal']
    return render_template('daily_planner.html',season=season, months=months, days=days, activities=activities)

@app.route('/weekly_planner')
def weekly_planner():
    activities = '''
* Read News Letter
* Lucy Time!
* Games with Ben
* Couples Bible study
* Chore
* Clean Garage
* Clean Desks
* Water Plants
* Swap Batteries'''.split('* ')[1:]
    dates = get_date_sequence(SUNDAY)
    return render_template('weekly_planner.html',season=season,activities=activities,weeks=dates)

@app.route('/monthly_recap')
def monthly_recap():
    return render_template('icon_list_sections.html',title='Monthly Recap',rows = 4, img='notebook.png',height='8',
                           sections=['January','February','March'])

@app.route('/celebrations')
def celebrations():
    return render_template('icon_list.html',title='Celebrations!',rows=21,img='tada.png',height='20')

@app.route('/hospitality')
def hospitality():
    rows = [
        ("Gigi Time", 3),
        ("Call Brady", 3),
        ("Call Nathan", 3),
        ("Date Night", 3),
    ]
    title = "Friends and Family"
    max_cells = max([row[1] for row in rows])
    return render_template('hospitality.html', rows=rows, title=title, max_cells=max_cells)

@app.route('/couples_bible_study')
def couples_bible_study():
    return render_template('weekly.html',weeks=get_date_sequence(SATURDAY), title='Couple\'s Bible Study')

@app.route('/house_projects')
def house_projects():
    return render_template('icon_list.html',title='House Projects',rows=11,img='checkedbox.png',height='60', background='handyman.png')

@app.route('/lucy_time')
def lucy_time():
    return render_template('weekly.html',weeks=get_date_sequence(TUESDAY), title='Lucy Time', background='playground.png')
    
@app.route('/unreal')
def unreal():
    return render_template('icon_list.html',title='Learning Unreal Engine 5',rows=12,img='unreal.png',height='40', background='unreal.png')

# Seasonal
@app.route('/bbqandbonfire')
def bbqandbonfire():
    return render_template('icon_list.html',title='BBQ and Bonfire',rows=11,img='bonfire.png',height='60', background='bonfire.png')
    
@app.route('/garden_hours')
def garden_hours():
    return render_template('blank.html',title='Hours Gardening',caption='Each leaf represents one hours work. <br/>Apples represent pounds of produce.', background='static/tree-no-leaves-drawing.png')

@app.route('/nano')
def nano():
    start = datetime.strptime('2023-11-01', '%Y-%m-%d')
    end = datetime.strptime('2023-11-30', '%Y-%m-%d')
    days = FULL_WEEK
    dates = get_specific_multi_date_sequence(days,start,end)

    units = ['Words']
    unit_steps = [range(0,5000,250)]
    return render_template('graph.html',dates=dates,title='NaNoWriMo',units=units,unit_steps=unit_steps)

@app.route('/advent_of_code')
def advent_of_code():
    start = datetime.strptime('2023-12-01', '%Y-%m-%d')
    end = datetime.strptime('2023-12-25', '%Y-%m-%d')
    days = FULL_WEEK
    dates = get_specific_multi_date_sequence(days,start,end)

    units = ['Minutes']
    unit_steps = [range(6,126,6)]
    return render_template('graph.html',dates=dates,title='Advent of Code',units=units,unit_steps=unit_steps)

@app.route('/dnd')
def dnd():
    return render_template('icon_list.html',title='Dungeons and Dragons Campaign',rows=16,img='d20.png',height='40')

# Exercise
@app.route('/ultimate_frisbee')
def ultimate_frisbee():
    return render_template('weekly.html',weeks=get_multi_date_sequence([SUNDAY]), title='Vermillion Friends Exercise Sundays', background='ultimate frisbee.png')
    
@app.route('/ultimate_frisbee2')
def ultimate_frisbee2():
    return render_template('weekly.html',weeks=get_multi_date_sequence([THURSDAY]), title='Vermillion Friends Exercise Thursdays', background='ultimate frisbee.png')

@app.route('/swimming')
def swimming():
    dates = get_multi_date_sequence([MONDAY,WEDNESDAY])
    #dates = get_date_sequence(TUESDAY)
    units = ['BPM','Laps']
    unit_steps = [range(120,200,4),range(20,40)]
    return render_template('graph.html',dates=dates,title='Lap Swimming',units=units,unit_steps=unit_steps)

@app.route('/running')
def running():
    dates = get_multi_date_sequence([MONDAY,WEDNESDAY])
    #dates = get_date_sequence(TUESDAY)
    units = ['BPM','Mi','Time']
    unit_steps = [range(120,200,4),[i/10.0 for i in range(20,40,1)], range(20,40,1)]
    return render_template('graph.html',dates=dates,title='Running',units=units,unit_steps=unit_steps)

@app.route('/discgolf')
def discgolf():
    dates = get_multi_date_sequence([FRIDAY])
    return render_template('disc.html',dates=dates)

@app.route('/arms')
def arms():
    dates = get_date_sequence(FRIDAY)
    items = ['Chest Press','Angel','Bicep Curl','Tricep Curl','Bent Over Row']
    steps = 5
    item_bounds = [[20,60],[10,45],[10,45],[10,45],[10,45]]
    item_intervals = [int((bound[1]-bound[0])/steps) for bound in item_bounds]
    item_units = []
    for i,bounds in enumerate(item_bounds):
        units = [bounds[1]]
        for j in range(steps-1):
            units.append(bounds[1] - item_intervals[i] * (j+1))
        item_units.append(units)
    return render_template('stacked_graph.html',dates=dates,title='Weight Lifting: Arms',items=items,
        item_units=item_units, steps=steps)

@app.route('/core')
def core():
    dates = get_date_sequence(TUESDAY)
    items = ['Planking','Shoulder Taps','90° Toe Taps','Glute Bridge','Cross Crunches']
    steps = 5
    item_bounds = [[60,120],[30,90],[150,250],[30,90],[120,210]]
    item_intervals = [int((bound[1]-bound[0])/steps) for bound in item_bounds]
    item_units = []
    for i,bounds in enumerate(item_bounds):
        units = [bounds[1]]
        for j in range(steps-1):
            units.append(bounds[1] - item_intervals[i] * (j+1))
        item_units.append(units)
    return render_template('stacked_graph.html',dates=dates,title='Core workout',items=items,
        item_units=item_units, steps=steps)

@app.route('/legs')
def legs():
    dates = get_date_sequence(TUESDAY)
    items = ['Planking','90° Toe Taps','Shoulder Taps','Degage','Cross Crunches']
    steps = 5
    item_bounds = [[60,120],[150,250],[30,90],[30,90],[120,210]]
    item_intervals = [int((bound[1]-bound[0])/steps) for bound in item_bounds]
    item_units = []
    for i,bounds in enumerate(item_bounds):
        units = [bounds[1]]
        for j in range(steps-1):
            units.append(bounds[1] - item_intervals[i] * (j+1))
        item_units.append(units)
    return render_template('stacked_graph.html',dates=dates,title='Leg Day!',items=items,
        item_units=item_units, steps=steps)

@app.route('/notes')
def notes():
    return render_template('icon_list.html',title='Notes',rows=21,img='notebook.png',height='20')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
