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
    pages = ['daily_planner','weekly_planner','quarter_goals','hospitality','couples_bible_study','thick_as_thieves',
        'prodev','projects','bible_mem','grilling','movies','swimming', 'website', 'misc_goals', 'notes']
    return render_template('index.html',pages=pages)

@app.route('/quarter_goals')
def quarter_goals():
    title = 'Summer 2021'
    subtitle = 'Season of Summer Vacation'
    goals = ['Brew a ginger bug','Play 3 new video games (min 3 hours)','Have a guys night','Read "Thick as Thieves"','Buy a Stock','Fix Lucy\'s car','Invite someone over','Draw twice a week','Swim 4 laps in 3 minutes','Learn to plumb','Get media to be stable','Get PDF publishing of journal working']
    return render_template('goals.html',title=title,goals=goals,subtitle=subtitle)

@app.route('/daily_planner/')
def daily_planner():
    season = "Summer 2021"
    ms = '%Y-%m'
    months = [datetime.strptime('2021-07', ms),datetime.strptime('2021-08', ms), datetime.strptime('2021-09', ms)]
    days = []
    day = delta(days=1)
    for month in months:
        temp_month = datetime.strptime(month.strftime(ms),ms)
        dc = 0
        while temp_month.month == month.month:
            temp_month += day
            dc += 1
        days.append(dc)
    activities = ['Update Journal','Japanese','Dishes','Exercise','Ab Exercises']
    return render_template('daily_planner.html',season=season, months=months, days=days, activities=activities)

@app.route('/weekly_planner')
def weekly_planner():
    season = 'Summer 2021'
    activities = ['Chore','House Project','Read News Letter','Men\'s Bible Study','Bible Memorization',
        'Couple\'s bible study','Games with Ben','Drawing 1','Drawing 2','Thick as Thieves','Swiming']
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
    date = datetime.strptime('2021-07-10', '%Y-%m-%d')
    dates = []
    week_delta = delta(days=7)
    weeks = 14
    for week in range(weeks):
        dates.append(date)
        date = date + week_delta
    return render_template('weekly.html',weeks=dates, title='House Projects')

@app.route('/prodev')
def prodev():
    date = datetime.strptime('2021-07-08', '%Y-%m-%d')
    dates = []
    week_delta = delta(days=7)
    weeks = 14
    for week in range(weeks):
        dates.append(date)
        date = date + week_delta
    return render_template('weekly.html',weeks=dates, title='Professional Development')

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


@app.route('/movies')
def movies():
    return render_template('icon_list.html',title='Movies',rows=12,img='movie_tape.png',height='50')

@app.route('/bible_mem')
def bible_mem():
    date1 = datetime.strptime('2021-07-04', '%Y-%m-%d')
    weeks = 14
    dates = []
    week_delta = delta(days=7)
    for i in range(weeks):
        dates.append(date1)
        date1 = date1 + week_delta
    units = ['Verses']
    unit_steps = [range(0,105,5)]
    return render_template('bible_verses.html',dates=dates,title='Bible Memorization', units=units,unit_steps=unit_steps)

@app.route('/couples_bible_study')
def couples_bible_study():
    return render_template('icon_list.html',title='Couple\'s Bible Study',rows=14,img='bible.png',height='50')

@app.route('/thick_as_thieves')
def thick_as_thieves():
    return render_template('icon_list.html',title='Thick as Thieves',rows=13,img='book.png',height='50',background='thick_as_thieves.jpg')
    
@app.route('/hospitality')
def hospitality():
    return render_template('hospitality.html')

@app.route('/misc_goals')
def misc_goals():
    return render_template('misc_goals.html')

@app.route('/grilling')
def grilling():
    return render_template('grilling.html')

@app.route('/swimming')
def swimming():
    date1 = datetime.strptime('2021-07-05', '%Y-%m-%d')
    date2 = datetime.strptime('2021-07-06', '%Y-%m-%d')
    date3 = datetime.strptime('2021-07-08', '%Y-%m-%d')
    date4 = datetime.strptime('2021-07-09', '%Y-%m-%d')
    weeks = 14
    dates = []
    week_delta = delta(days=7)
    for i in range(weeks):
#        dates.append(date1)
#        dates.append(date2)
#        dates.append(date3)
#        dates.append(date4)
#        date1 = date1 + week_delta
#        date2 = date2 + week_delta
#        date3 = date3 + week_delta
#        date4 = date4 + week_delta
        dates.append(date1)
        dates.append(date1)
#        dates.append(date1)
        date1 = date1 + week_delta
    units = ['Heart Rate (BPM)','Distance (Laps)','Lap Time (s)']
    unit_steps = [range(100,180,4),[v for v in range(8,30)],range(30,112,4)]
    return render_template('graph.html',dates=dates,title='Swimming',units=units,unit_steps=unit_steps)

@app.route('/website')
def website():
    return render_template('icon_list.html',title='Coding: Personal website redesign',rows=14,img='www.png',height='50')

@app.route('/notes')
def notes():
    return render_template('icon_list.html',title='Notes',rows=21,img='notebook.png',height='20')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
