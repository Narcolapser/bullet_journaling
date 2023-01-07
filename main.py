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
* Clean and organize under stairs shelves
* Freeze Credit
* Use or Dispose of sassafrass tea
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
* Catchup Task
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

@app.route('/screwtape')
def religionbook():
    return render_template('icon_list.html',title='The Screwtape Letters',rows=25,img='book.png',height='15',background='screwtape.jpeg')


@app.route('/dragon')
def dragon():
    sections = [['Chapter 4',[('Pages',279)]],['Chapter 5',[('Pages',343)]],['Chapter 6',[('Pages',389)]],['Chapter 7',[('Pages',463)]],['Chapter 8',[('Pages',513)]],['Chapter 9',[('Pages',585)]],['Chapter 10',[('Pages',723)]],['Chapter 11',[('Pages',733)]],['Chapter 12',[('Pages',745)]]]
    return render_template('bars.html',title='Dragon Book',sections=sections)

@app.route('/house_projects')
def house_projects():
    return render_template('icon_list.html',title='House Projects',rows=10,img='checkedbox.png',height='60', background='handyman.png')

@app.route('/movies')
def movies():
    return render_template('weekly.html',weeks=get_date_sequence(SUNDAY), title='Movies', background='popcorn.png')

@app.route('/lucy_time')
def lucy_time():
    return render_template('weekly.html',weeks=get_date_sequence(TUESDAY), title='Lucy Time', background='playground.png')

@app.route('/sensors')
def sensors():
    return render_template('icon_list.html',title='Sensor Projects',rows=24,img='sensor.png',height='15',background='sensor.png')

@app.route('/boardgames')
def boardgames():
    entry = {'title': '__________________________', 'image_url':'http://localhost:5000/static/d20.png', 'extra':'☆☆☆☆☆'}
    items = [entry for i in range(6)]
    return render_template('item_grid.html', title='New Boardgames', items=items, columns=2)

@app.route('/seedlings')
def seedlings():
    entry = {'title': '__________________________', 'image_url':'http://localhost:5000/static/seedling.jpg', 'extra':'Prep Time:_________________'}
    items = [entry for i in range(12)]
    return render_template('item_grid.html', title='Seedling plantings', items=items, columns=3)
    
@app.route('/computing')
def computing():
    items = [
        {'title': 'Migrate off of gmail', 'image_url':'https://clipartcraft.com/images/gmail-logo-transparent-8.png'},
        {'title': 'Build out backups', 'image_url':'http://localhost:5000/static/nas.svg'},
        {'title': 'Budget Automations: Ace', 'image_url':'https://thehardwareconnection.com/wp-content/uploads/2020/06/Ace-logo.jpg'},
        {'title': 'Budget Automations: Hyvee', 'image_url':'https://shelbyreport.nyc3.cdn.digitaloceanspaces.com/wp-content/uploads/2019/06/HY-VEE.png'},
        {'title': 'Recreate Personal Website', 'image_url':'http://localhost:5000/static/www.png'},
        {'title': 'Improve Bullet Journal Software', 'image_url':'http://localhost:5000/static/notebook.png'}
    ]
    return render_template('item_grid.html', title='Computing', items=items, columns=2)

@app.route('/electronics')
def electronics():
    items = [
        {'title': 'Re-Do the Ther-Mom-eter', 'image_url':'https://clipartcraft.com/images/thermometer-clipart-transparent-background-2.png'},
        {'title': 'Cases for Distributed Nodes', 'image_url':'https://media.istockphoto.com/vectors/adapter-vector-id1245795116?k=6&m=1245795116&s=170667a&w=0&h=Wv1VYYM2ulWzjfHg5GkpVJJtdlYsihp8F4sBf9ZHq9g='},
        {'title': 'Finish Computer', 'image_url':'https://images.cdn4.stockunlimited.net/clipart/computer-cabinet_1614954.jpg'},
        {'title': 'Decide on 433mhz', 'image_url':'http://localhost:5000/static/Radio Tower.png'},
        {'title': 'Batter+Solar Project', 'image_url':'http://localhost:5000/static/battery.png'},
        {'title': 'Finish Thor', 'image_url':'http://localhost:5000/static/current_warning.png', 'extra':'Draw power from within!'}
    ]
    return render_template('item_grid.html', title='Electronics', items=items, columns=2)
    
@app.route('/Preping')
def Preping():
    items = [
        {'title': 'Print and Sign Wills', 'image_url':'https://media.istockphoto.com/vectors/signed-last-will-rgb-color-icon-document-with-stamp-notarized-and-vector-id1225537357?k=6&m=1225537357&s=612x612&w=0&h=j-SKPHODecbNo_LT5cB5qiczgRFENKO5ID7cVswRM28='},
        {'title': 'Compile Retirement Info', 'image_url':'https://media.istockphoto.com/illustrations/flat-round-icon-illustration-id517173627?k=6&m=517173627&s=612x612&w=0&h=1Xlb8G7mX-VeqO6D-U4iNSdu6Tob4P5KEVjKNLDDy4E='},
        {'title': 'Move funds out of SDRS-SRP', 'image_url':'https://media.istockphoto.com/vectors/map-of-the-us-state-of-south-dakota-vector-id1189596183?k=6&m=1189596183&s=612x612&w=0&h=3HU4fCjjvBgVcwvS6_NJjNc1b3yfarENESTUKNLfy0g='},
        {'title': 'Life Insurance Beneficiaries', 'image_url':'https://media.istockphoto.com/illustrations/life-insurance-stamp-illustration-id468291652?k=6&m=468291652&s=612x612&w=0&h=uLx9qVj1BVDIRA0EGaCkbVh5lqPijKVAVRVLwH32PcM='},
        {'title': 'ESOP Beneficiaries', 'image_url':'http://localhost:5000/static/esop.jpg'},
        {'title': 'Update Info in Firesafe', 'image_url':'https://etc.usf.edu/clipart/19100/19122/safe_19122_md.gif'}
    ]
    return render_template('item_grid.html', title='Preping', items=items, columns=2)

@app.route('/biking')
def bike():
    dates = get_multi_date_sequence([TUESDAY,FRIDAY])
    #dates = get_date_sequence(TUESDAY)
    units = ['BPM','Time']
    unit_steps = [range(120,200,4),range(20,40)]
    return render_template('graph.html',dates=dates,title='Biking',units=units,unit_steps=unit_steps)

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
    items = ['90° Toe Taps','Frappes','Knee Pushes','Passe','Cross Crunches']
    steps = 5
    item_bounds = [[70,150],[45,90],[70,150],[30,90],[70,150]]
    item_intervals = [int((bound[1]-bound[0])/steps) for bound in item_bounds]
    item_units = []
    for i,bounds in enumerate(item_bounds):
        units = [bounds[1]]
        for j in range(steps-1):
            units.append(bounds[1] - item_intervals[i] * (j+1))
        item_units.append(units)
    return render_template('stacked_graph.html',dates=dates,title='Leg Day!',items=items,
        item_units=item_units, steps=steps)

@app.route('/handball')
def handball():
    return render_template('weekly.html',weeks=get_date_sequence(THURSDAY), title='Handball', background='handball.png')

@app.route('/notes')
def notes():
    return render_template('icon_list.html',title='Notes',rows=21,img='notebook.png',height='20')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
