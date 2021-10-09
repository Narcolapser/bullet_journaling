import requests
import json
from flask import Flask, render_template, request, send_file
from datetime import datetime, timedelta as delta

app = Flask(__name__)

@app.route('/')
def root():
#    pages = ['daily_planner','weekly_planner','projects','prodev','drawing','spring_goals','movies',
#             'disc','bitcoin','running','crypto_investing','bible_mem','hospitality','misc_goals',
#             'yearly_goals','video_games','board_games','camping','themes','archery','body_fat',
#             'notes','cover']
#    pages = ['daily_planner','weekly_planner','quarter_goals','hospitality','couples_bible_study','thick_as_thieves',
#        'prodev','projects','bible_mem','grilling','movies','swimming', 'website', 'misc_goals', 'notes']
    pages = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods:
            pages.append(rule.endpoint)
    return render_template('index.html',pages=pages)

@app.route('/quarter_goals')
def quarter_goals():
    title = 'Summer 2021'
    subtitle = 'Season of Privacy'
    goals = ['Migrate off of gMail to ProtonMail','Migrate existing online services to an email proxy',
        'Try 3 New Board Games','Try 3 new Video Games','Upgrade home WiFi','Clean up Bitwarden','Plan Weight Bench']
    return render_template('goals.html',title=title,goals=goals,subtitle=subtitle)

@app.route('/daily_planner/')
def daily_planner():
    season = "Fall 2021"
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
    activities = ['Update Journal','Spanish','Dishes','Exercise']
    return render_template('daily_planner.html',season=season, months=months, days=days, activities=activities)

@app.route('/weekly_planner')
def weekly_planner():
    season = 'Summer 2021'
    activities = ['Chore','House Project','Read News Letter','Men\'s Bible Study','Bible reading',
        'Couple\'s bible study','Games with Ben','Return of the thief']
    weeks = []
    date = datetime.strptime('2021-07-04', '%Y-%m-%d')
    week_delta = delta(days=7)
    weeks = 14
    dates = []
    for week in range(weeks):
        dates.append(date)
        date = date + week_delta
    return render_template('weekly_planner.html',season=season,activities=activities,weeks=dates)

@app.route('/projects')
def house_projects():
    date = datetime.strptime('2021-10-16', '%Y-%m-%d')
    dates = []
    week_delta = delta(days=7)
    weeks = 12
    for week in range(weeks):
        dates.append(date)
        date = date + week_delta
    return render_template('weekly.html',weeks=dates, title='House Projects')


@app.route('/movies')
def movies():
    return render_template('icon_list.html',title='Movies',rows=12,img='movie_tape.png',height='50')


@app.route('/couples_bible_study')
def couples_bible_study():
    return render_template('icon_list.html',title='Couple\'s Bible Study:\n The 10 Most Misunderstood Verses in the Bible',rows=10,img='bible.png',height='50')

@app.route('/reading')
def thick_as_thieves():
    return render_template('icon_list.html',title='Return of the Thief',rows=13,img='book.png',height='50',background='thick_as_thieves.jpg')
    
@app.route('/hospitality')
def hospitality():
    return render_template('hospitality.html')

@app.route('/misc_goals')
def misc_goals():
    return render_template('misc_goals.html')

@app.route('/Running')
def swimming():
    date1 = datetime.strptime('2021-07-05', '%Y-%m-%d')
    date2 = datetime.strptime('2021-07-06', '%Y-%m-%d')
    date3 = datetime.strptime('2021-07-08', '%Y-%m-%d')
    date4 = datetime.strptime('2021-07-09', '%Y-%m-%d')
    weeks = 12
    dates = []
    week_delta = delta(days=7)
    for i in range(weeks):
        dates.append(date1)
        dates.append(date1)
#        dates.append(date1)
        date1 = date1 + week_delta
    units = ['BPM','Miles','Time']
    unit_steps = [range(100,180,4),[v for v in range(8,30)],range(30,112,4)]
    return render_template('graph.html',dates=dates,title='Running',units=units,unit_steps=unit_steps)

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

@app.route('/notes')
def notes():
    return render_template('icon_list.html',title='Notes',rows=21,img='notebook.png',height='20')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
