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

@app.route('/quarter_goals')
def quarter_goals():
    title = 'Summer 2021'
    subtitle = 'Season of Privacy'
    goals = ['Migrate off of gMail to ProtonMail','Setup email proxying',
        'Try 3 New Board Games','Try 3 new Video Games','Upgrade home WiFi','Clean up Bitwarden','Plan Weight Bench',
        'Get FOSS plackards made for office', 'Shape website redesign project', 'Read "Becoming Invisible"',
        'Setup Kodi','Finish Computer','Install Mushroom buttons in garage','Clean garage',
        'Touchplate Lights in Homeassistant', 'Improve bullet journal software']
    return render_template('goals.html',title=title,goals=goals,subtitle=subtitle)

@app.route('/daily_planner/')
def daily_planner():
    ms = '%Y-%m'
    months = [datetime.strptime('2021-10-10', ms+'-%d'),datetime.strptime('2021-11', ms), datetime.strptime('2021-12', ms)]
    days = []
    day = delta(days=1)
    for month in months:
        temp_month = datetime.strptime(month.strftime(ms),ms)
        dc = 0
        while temp_month.month == month.month:
            temp_month += day
            dc += 1
        days.append(dc)
    activities = ['Update Journal','Spanish','Dishes','Exercise','Bible']
    return render_template('daily_planner.html',season=season, months=months, days=days, activities=activities)

@app.route('/weekly_planner')
def weekly_planner():
    activities = ['Chore','Clean Desk','House Project','Disc','Running','Read News Letter','Men\'s Bible Study',
        'Couple\'s bible study','Games with Ben','Return of the thief']
    weeks = []
    dates = get_date_sequence(0)
    return render_template('weekly_planner.html',season=season,activities=activities,weeks=dates)

@app.route('/house_projects')
def house_projects():
    date = datetime.strptime('2021-10-16', '%Y-%m-%d')
    dates = []
    week_delta = delta(days=7)
    weeks = 11
    for week in range(weeks):
        dates.append(date)
        date = date + week_delta
    return render_template('weekly.html',weeks=dates, title='House Projects')


@app.route('/movies')
def movies():
    return render_template('icon_list.html',title='Movies',rows=12,img='movie_tape.png',height='50')


@app.route('/couples_bible_study')
def couples_bible_study():
    return render_template('icon_list.html',title='Couple\'s Bible Study:</br> The 10 Most Misunderstood Verses in the Bible',rows=10,img='bible.png',height='50')


@app.route('/reading')
def reading():
    return render_template('icon_list.html',title='Return of the Thief:</br>The Book of Pheris, Vol I',rows=8,img='book.png',height='25',background='return of the thief.jpeg')


@app.route('/reading2')
def reading2():
    return render_template('icon_list.html',title='Return of the Thief:</br>The Book of Pheris, Vol II',rows=14,img='book.png',height='25',background='return of the thief.jpeg')
    
@app.route('/hospitality')
def hospitality():
    return render_template('hospitality.html')

@app.route('/misc_goals')
def misc_goals():
    return render_template('misc_goals.html')

@app.route('/Running')
def Running():
#    date1 = datetime.strptime('2021-10-11', '%Y-%m-%d')
#    date2 = datetime.strptime('2021-10-14', '%Y-%m-%d')
#    weeks = 12
#    dates = []
#    week_delta = delta(days=7)
#    for i in range(weeks):
#        dates.append(date1)
#        dates.append(date2)
#        date1 = date1 + week_delta
#        date2 = date2 + week_delta
    dates = get_multi_date_sequence([1,3])
    units = ['BPM','Miles','Time']
    unit_steps = [range(100,180,4),[v/10.0 for v in range(15,35)],range(10,30)]
    return render_template('graph.html',dates=dates,title='Running',units=units,unit_steps=unit_steps)

@app.route('/ringfit')
def ringfit():
    date1 = datetime.strptime('2021-10-13', '%Y-%m-%d')
    date2 = datetime.strptime('2021-10-15', '%Y-%m-%d')
    weeks = 12
    dates = []
    week_delta = delta(days=7)
    for i in range(weeks):
        dates.append(date1)
        dates.append(date2)
        date1 = date1 + week_delta
        date2 = date2 + week_delta
    units = ['BPM','Distance','Calories']
    unit_steps = [range(100,180,4),[v/10.0 for v in range(0,20)],range(10,30)]
    return render_template('graph.html',dates=dates,title='Ring Fit',units=units,unit_steps=unit_steps)

@app.route('/disc')
def disc():
    date1 = datetime.strptime('2021-10-12', '%Y-%m-%d')
    weeks = 12
    dates = []
    week_delta = delta(days=7)
    for i in range(weeks):
        dates.append(date1)
        date1 = date1 + week_delta
    return render_template('disc.html',dates=dates)

@app.route('/incognito')
def incognito():
    rows = 14
    cols = 2
    title = 'Go Incognito Lessons'
    picture = 'techlore.jpg'
    row_titles = [f'{i*2+1} & {i*2+2}' for i in range(rows-1)] + ['27']
    return render_template('picture_grid.html',rows=rows, cols=cols, title=title, picture=picture, row_titles=row_titles, pic_width=15)
    
@app.route('/drawing')
def drawing():
    date = datetime.strptime('2021-07-04', '%Y-%m-%d')
    dates = []
    week_delta = delta(days=7)
    weeks = 14
    for week in range(weeks):
        dates.append(date)
        date = date + week_delta

    row_titles = [date.strftime('%b %d') for date in dates]
    rows = 14
    cols = 2
    title = "Drawing"
    picture = 'drawing.png'
    return render_template('picture_grid.html',rows=rows, cols=cols, title=title, picture=picture, row_titles=row_titles, pic_width=20)

@app.route('/monthly_recap')
def monthly_recap():
    return render_template('icon_list_sections.html',title='Monthly Recap',rows = 7, img='notebook.png',height='12',
                           sections=['October','November','December'])
@app.route('/notes')
def notes():
    return render_template('icon_list.html',title='Notes',rows=21,img='notebook.png',height='20')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
