import requests
import json
from flask import Flask, render_template, request, send_file
from datetime import datetime, timedelta as delta

app = Flask(__name__)

@app.route('/')
def root():
    pages = ['daily_planner','weekly_planner','projects','prodev','drawing','yearly_goals','spring_goals',
             'disc','bitcoin','running']
    return render_template('index.html',pages=pages)

#@app.route('/static/<item>')
#def static(item):
#    return send_file(f'/static/{item}')

@app.route('/weekly/<start>/<weeks>')
def weekly(start, weeks):
    date = datetime.strptime(start, '%Y-%m-%d')
    dates = []
    week_delta = delta(days=7)
    weeks = int(weeks)
    for week in range(weeks):
        dates.append(date)
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
    activities = ['Spanish','Dishes','Exercise','Ab Exercises']
    return render_template('daily_planner.html',season=season, months=months, days=days, activities=activities)

@app.route('/weekly_planner')
def weekly_planner():
    season = 'Spring 2021'
    activities = ['Chore','House Project','Read News Letter','Men\'s Bible Study','Bible Memorization','Games with Ben','Drawing','Reading Bitcoin Book','Disc Golf']
    weeks = []
    date = datetime.strptime('2021-04-04', '%Y-%m-%d')
    week_delta = delta(days=7)
    weeks = 12
    dates = []
    for week in range(weeks):
        dates.append(date)
        date = date + week_delta
    return render_template('weekly_planner.html',season=season,activities=activities,weeks=dates)

@app.route('/projects')
def house_projects():
    date = datetime.strptime('2021-04-10', '%Y-%m-%d')
    dates = []
    week_delta = delta(days=7)
    weeks = 12
    for week in range(weeks):
        dates.append(date)
        date = date + week_delta
    return render_template('weekly.html',weeks=dates, title='House Projects')

@app.route('/prodev')
def prodev():
    date = datetime.strptime('2021-04-08', '%Y-%m-%d')
    dates = []
    week_delta = delta(days=7)
    weeks = 12
    for week in range(weeks):
        dates.append(date)
        date = date + week_delta
    return render_template('weekly.html',weeks=dates, title='Professional Development')

@app.route('/drawing')
def drawing():
    date = datetime.strptime('2021-04-04', '%Y-%m-%d')
    dates = []
    week_delta = delta(days=7)
    weeks = 12
    for week in range(weeks):
        dates.append(date)
        date = date + week_delta

    row_titles = [date.strftime('%b %d') for date in dates]
    rows = 12
    cols = 2
    title = "Drawing"
    picture = 'drawing.png'
    return render_template('picture_grid.html',rows=rows, cols=cols, title=title, picture=picture, row_titles=row_titles, pic_width=10)

@app.route('/yearly_goals')
def yearly_goals():
    title = '2021 Goals'
    goals = ['Learn to plumb','Draw 80 times','Brew a Rootbeer with a Gingerbug','Play 12 new video games','play 12 new board/card games','Read all of Harry Potter','Daily language lessons','Develop a six pack','Monthly Call w/ brady','Monthly Gigi time','Monthly tarts','Quarterly guys night','Do some freelance devops/dev work','Invest in stocks and crypto','Finish "Queens Theif" series','Read "Bitcoin for the Befuddled"','Setup Bible memorization scheme','Memorize several chunks of the Bible','Read a theology book','Beat ringfit','Track body fat','Run twice a week in summer','Teach Lucy "swim"','Make Lucy a mud kitchen','Get Lucy\'s car working']
    return render_template('goals.html',title=title,goals=goals)

@app.route('/spring_goals')
def spring_goals():
    title = 'Spring 2021'
    subtitle = 'Season of Enjoying'
    goals = ['Brew a root beer with ginger bug','Play 3 new video games (min 3 hours)','Have a guys night','Read "Bitcoin for the Befuddled"','Invest in some Cryptos','Design Bible Memorization scheme','Fix Lucy\'s car','Invite someone over','Beat Prentis in 30 throws','Draw twice a week']
    return render_template('goals.html',title=title,goals=goals,subtitle=subtitle)

@app.route('/disc')
def disc():
    date1 = datetime.strptime('2021-04-06', '%Y-%m-%d')
    date2 = datetime.strptime('2021-04-09', '%Y-%m-%d')
    weeks = 12
    dates = []
    week_delta = delta(days=7)
    for i in range(weeks):
        dates.append(date1)
        dates.append(date2)
        date1 = date1 + week_delta
        date2 = date2 + week_delta
    return render_template('disc.html',dates=dates)

@app.route('/bitcoin')
def bitcoin():
    rows = 4
    cols = 3
    title = "Bitcoin for the Befuddled"
    picture = 'bitcoin.png'
    return render_template('picture_grid.html',rows=4, cols=3, title=title, picture=picture)

@app.route('/running')
def running():
    date1 = datetime.strptime('2021-04-05', '%Y-%m-%d')
    date2 = datetime.strptime('2021-04-07', '%Y-%m-%d')
    weeks = 12
    dates = []
    week_delta = delta(days=7)
    for i in range(weeks):
        dates.append(date1)
        dates.append(date2)
        date1 = date1 + week_delta
        date2 = date2 + week_delta
    units = ['Heart Rate (BPM)','Distance (M)','Time (m)']
    unit_steps = [range(100,180,4),[v/10.0 for v in range(10,30)],range(10,30)]
    return render_template('graph.html',dates=dates,title='Running',units=units,unit_steps=unit_steps)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
