import requests
import json
from flask import Flask, render_template, request, send_file
from datetime import datetime, timedelta as delta

app = Flask(__name__)

year = '2023'
season = f'Spring {year}'

# The first sunday of the quarter
sdate = datetime.strptime('2023-04-02', '%Y-%m-%d')

# The last saturday of the quarter
fdate = datetime.strptime('2023-05-27', '%Y-%m-%d')


SUNDAY = 0
MONDAY = 1
TUESDAY = 2
WEDNESDAY = 3
THURSDAY = 4
FRIDAY = 5
SATURDAY = 6

def get_specific_multi_date_sequence(days_of_week,start,end):
    dow_list = [start + delta(days=dow) for dow in days_of_week]
    week_delta = delta(days=7)
    dates = []
    while dow_list[0] <= end:
        for i,date in enumerate(dow_list):
            dates.append(date)
            dow_list[i] = date + week_delta
    return dates

def get_multi_date_sequence(days_of_week):
    return get_specific_multi_date_sequence(sdate,fdate)

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
    
    col1 = get_specific_multi_date_sequence([SUNDAY,MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY], sdate1, fdate1)
    col2 = get_specific_multi_date_sequence([SUNDAY,MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY], sdate2, fdate2)
    col3 = get_specific_multi_date_sequence([SUNDAY,MONDAY,TUESDAY,WEDNESDAY,THURSDAY,FRIDAY,SATURDAY], sdate3, fdate3)
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


# Quarter Pages
@app.route('/quarter_goals')
def quarter_goals():
    subtitle = 'Season of Nothing New'
    goals = [goal.replace('\n','') for goal in '''
* Reread Dreaming In code
* Habitica Weeklies do damage
* Habitica rewards in HA
* Auto receipts server running
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
    activities = ['Isaiah', 'Dishes','Exercise','Update Journal']
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
    return render_template('icon_list_sections.html',title='Monthly Recap',rows = 7, img='notebook.png',height='12',
                           sections=['February','March'])

@app.route('/celebrations')
def celebrations():
    return render_template('icon_list.html',title='Celebrations!',rows=21,img='tada.png',height='20')

@app.route('/hospitality')
def hospitality():
    return render_template('hospitality.html')

@app.route('/couples_bible_study')
def couples_bible_study():
    return render_template('weekly.html',weeks=get_date_sequence(SATURDAY), title='Couple\'s Bible Study')

@app.route('/religionbook')
def religionbook():
    return render_template('icon_list.html',title='The Screwtape Letters',rows=31,img='book.png',height='15',background='screwtape.jpeg')


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
    return render_template('weekly.html',weeks=get_date_sequence(TUESDAY), title='Lucy Time', background='dalle - snow playing.png')

@app.route('/sensors')
def sensors():
    return render_template('icon_list.html',title='Sensor Projects',rows=24,img='sensor.png',height='15',background='sensor.png')

@app.route('/boardgames')
def boardgames():
    entry = {'title': '__________________________', 'image_url':'http://localhost:5000/static/d20.png', 'extra':'☆☆☆☆☆'}
    items = [entry for i in range(6)]
    col_num = 2
    rows = [items[i:i+col_num] for i in range(0, len(items), col_num)]
    return render_template('item_grid.html', title='New Boardgames', rows=rows)

@app.route('/seedlings')
def seedlings():
    entry = {'title': 'Plant:__________________', 'image_url':'http://localhost:5000/static/seedling.jpg', 'extra':'Prep Time:_____________'}
    items = [entry for i in range(12)]
    col_num = 3
    rows = [items[i:i+col_num] for i in range(0, len(items), col_num)]
    return render_template('item_grid.html', title='Seedling plantings', rows=rows)
    
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
    col_num = 2
    rows = [items[i:i+col_num] for i in range(0, len(items), col_num)]
    return render_template('item_grid.html', title='Computing', rows=rows)

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
    col_num = 2
    rows = [items[i:i+col_num] for i in range(0, len(items), col_num)]
    return render_template('item_grid.html', title='Electronics', rows=rows)
    
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
    col_num = 2
    rows = [items[i:i+col_num] for i in range(0, len(items), col_num)]
    return render_template('item_grid.html', title='Preping', rows=rows)

@app.route('/biking')
def biking():
    dates = get_multi_date_sequence([TUESDAY,FRIDAY])
    #dates = get_date_sequence(TUESDAY)
    units = ['BPM','Time']
    unit_steps = [range(120,200,4),range(20,40)]
    return render_template('graph.html',dates=dates,title='Biking',units=units,unit_steps=unit_steps)

@app.route('/arms')
def arms():
    dates = get_date_sequence(MONDAY)
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
    dates = get_date_sequence(WEDNESDAY)
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
