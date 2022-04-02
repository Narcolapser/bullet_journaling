import requests
import json
from flask import Flask, render_template, request, send_file
from datetime import datetime, timedelta as delta

app = Flask(__name__)

year = '2022'
season = f'Spring {year}'

# The first sunday of the quarter
sdate = datetime.strptime('2022-04-03', '%Y-%m-%d')

# The last saturday of the quarter
fdate = datetime.strptime('2022-07-02', '%Y-%m-%d')


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

# Annual pages
@app.route('/title_page')
def title_page():
    return render_template('cover.html')

@app.route('/annual_goals')
def annual_goals():
    goals = [goal.replace('\n','') for goal in '''
* Learn Ham Radio
* Camp More
* Visit as many of the 19 parks Megan has listed as possible.
* Read 8 Books
* Print a Gun
* Finish Computer
* Read "Crossing on Time"
* Read CS books on my self that I never got around to
* Setup Server in Basement
* Create a game in unreal engine
* Demo a game on switch.
'''.split('* ')[1:]]
    return render_template('goals.html',title='Annual Goals',goals=goals,subtitle='')

@app.route('/themes_page')
def themes_page():
    return render_template('icon_list.html',title='Themes',rows=4,img='rainbow.png',height='150')

@app.route('/camping')
def camping():
    return render_template('icon_list.html',title='Camping',rows=6,img='tent.png',height='80')

@app.route('/parks')
def parks():
    return render_template('icon_list.html',title='Parks',rows=20,img='tree and table.png',height='30')

@app.route('/body')
def body():
    months = ['April','May','June','July','August','September','October','November','December','January','February','March']
    return render_template('body_fat.html',year=year,months=months)

@app.route('/new_games')
def vodogams():
    return render_template('icon_list.html',title='New Video Games',rows=12,img='d20.png',height='40')

@app.route('/events')
def events():
    return render_template('icon_list.html',title='Notable Events',rows=12,img='calendar.jpg',height='40')

# Quarter Pages
@app.route('/quarter_goals')
def quarter_goals():
    subtitle = 'Season of Automation v2'
    goals = [goal.title().replace('\n','') for goal in '''
* Organize Desk
* Recreate Personal Website
* Improve Bullet Journal Software
* Wire new outlet for sump pump
* Cover Sump
* Design Refined Computer Case
* Get Lucy's Wine from Joe
* Replace light in bathroom
* Learn to Plumb: Lucy's Mud Kitchen
* Learn to Plumb: Shower Fixtures
* Learn to Plumb: Valve to mainfloor bath
'''.split('* ')[1:]]
    return render_template('goals.html',title=season,goals=goals,subtitle=subtitle)

@app.route('/auto')
def auto():
    subtitle = 'Automation Task'
    goals = [goal.title().replace('\n','') for goal in '''
* Tracking Electricity Usage
* Tracking Water Usage
* Tracking Gas Usage
* Garage Door - Position
* Garage Door - Open
* Setup 433mhz Sensors
* Wireless Switch - Mainfloor Vanity
* Wireless Switch - Upstairs Vanity
* Pantry Lights
* 3D Printer
* TV Controlled From Home Assistant
* Door Sensors
* Window Sensors
* Thermometers Scattered Around
* Smartify Remaining lights
'''.split('* ')[1:]]
    return render_template('goals.html',title=subtitle,goals=goals)

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
    activities = ['Update Journal', 'Spanish', 'Dishes','Exercise','Bible']
    return render_template('daily_planner.html',season=season, months=months, days=days, activities=activities)

@app.route('/weekly_planner')
def weekly_planner():
    activities = ['Chore','Clean Desks','House Project','Read News Letter','Games with Ben']
    dates = get_date_sequence(SUNDAY)
    return render_template('weekly_planner.html',season=season,activities=activities,weeks=dates)

@app.route('/monthly_recap')
def monthly_recap():
    return render_template('icon_list_sections.html',title='Monthly Recap',rows = 7, img='notebook.png',height='12',
                           sections=['April','May','June'])

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
    
@app.route('/microservices')
def reading3():
    return render_template('icon_list.html',title='Building Microservices',rows=16,img='book.png',height='23',background='building_microservices.jpg')

@app.route('/cc')
def cc():
    return render_template('icon_list.html',title='Case for Christ',rows=15,img='book.png',height='23',background='caseforchrist.jpg')

@app.route('/celebrations')
def celebrations():
    return render_template('icon_list.html',title='Celebrations!',rows=21,img='tada.png',height='20')

@app.route('/lucy_time')
def lucy_time():
    return render_template('weekly.html',weeks=get_date_sequence(TUESDAY), title='Lucy Time', background='playground.png')

@app.route('/run')
def run():
    dates = get_multi_date_sequence([MONDAY,THURSDAY])
    #dates = get_date_sequence(TUESDAY)
    units = ['Miles','BPM','Time']
    unit_steps = [[float(i)/10 for i in range(16,35)],range(100,180,4),range(11,31)]
    return render_template('graph.html',dates=dates,title='Running',units=units,unit_steps=unit_steps)

@app.route('/pixels')
def pixels():
    emotions = ['Happy','Sad','Anxious','Angry','Excited','Productive','Stressed','Relaxed']
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
    
@app.route('/swim')
def swim():
    dates = get_multi_date_sequence([TUESDAY,FRIDAY])
    #dates = get_date_sequence(TUESDAY)
    units = ['Laps','BPM','Time']
    unit_steps = [range(12,33),range(100,180,4),range(11,31)]
    return render_template('graph.html',dates=dates,title='Swim',units=units,unit_steps=unit_steps)

@app.route('/arms')
def arms():
    dates = get_date_sequence(TUESDAY)
    items = ['Chest Press','Angel','Bicep Curl','Tricep Curl','Bent Over Row']
    steps = 5
    item_bounds = [[10,30],[10,30],[10,30],[10,30],[10,30]]
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
    dates = get_date_sequence(THURSDAY)
    items = ['Glute Bridge','Goblet Squats','Farmers Carry','Weighted Lounges','Step Ups']
    steps = 5
    item_bounds = [[10,30],[10,30],[10,30],[10,30],[10,30]]
    item_intervals = [int((bound[1]-bound[0])/steps) for bound in item_bounds]
    item_units = []
    for i,bounds in enumerate(item_bounds):
        units = [bounds[1]]
        for j in range(steps-1):
            units.append(bounds[1] - item_intervals[i] * (j+1))
        item_units.append(units)
    return render_template('stacked_graph.html',dates=dates,title='Weight Lifting: Arms',items=items,
        item_units=item_units, steps=steps)

@app.route('/notes')
def notes():
    return render_template('icon_list.html',title='Notes',rows=21,img='notebook.png',height='20')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
