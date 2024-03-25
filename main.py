import requests
import json
from flask import Flask, render_template, request, send_file
from datetime import datetime, timedelta as delta

from pages.util import Day_Of_Week, get_date_sequence, StartFinish
from pages.exercises import build_core, build_running
from pages.basics import build_notes, build_icon_list, build_weekly

app = Flask(__name__)

year = '2024'
season = f'Spring {year}'

# The first sunday of the quarter
sdate = datetime.strptime('2024-04-01', '%Y-%m-%d')

# The last saturday of the quarter
fdate = datetime.strptime('2024-05-31', '%Y-%m-%d')
dates = StartFinish(sdate, fdate)

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


# Quarter Pages - Recurring
@app.route('/quarter_goals')
def quarter_goals():
    subtitle = 'Season of Exodus'
    why_theme = 'The dominant feature of this quarter is the Exodus 90 challenge. It represents the majority the guidance for what I will be doing, or not doing, this quarter. Why I am doing this is to provide myself with an opportunity to grow in spirit with Christ. I wish to draw near to God and learn how to pray. Doing this challenge with the other men of my group I hope will encourage this growth. The goals below are ancillary to the theme, things to spend my time on productively while I am in this period of fasting.'
    goals = [goal.replace('\n','') for goal in '''
* Learn to use my Sextant
* Winter Camp
* Organize Bulk Spice Storage
* Develop Compost Plan
* Develop Garden Plan for next year
* Design a processor in Cedar Logic
* Flash Dreame to custom firmware
'''.split('* ')[1:]]
    return render_template('goals.html',title=season,goals=goals,subtitle=subtitle,why_theme=why_theme)

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
    activities = ['Quiet Hour', 'Dishes','Exercise','Walk Garden','Update Journal']
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
    dates = get_date_sequence(Day_Of_Week.SUNDAY)
    return render_template('weekly_planner.html',season=season,activities=activities,weeks=dates)

@app.route('/monthly_recap')
def monthly_recap():
    return render_template('icon_list_sections.html',title='Monthly Recap',rows = 7, img='notebook.png',height='8',
                           sections=['January','February','March'])

@app.route('/celebrations')
def celebrations():
    return render_template('icon_list.html',title='Celebrations!',rows=21,img='tada.png',height='20')


@app.route('/couples_bible_study')
def couples_bible_study():
    return render_template('weekly.html',weeks=get_date_sequence(Day_Of_Week.SATURDAY), title='Couple\'s Bible Study', background='../bible.png')

@app.route('/house_projects')
def house_projects():
    return render_template('icon_list.html',title='House Projects',rows=11,img='checkedbox.png',height='60', background='handyman.png')

@app.route('/lucy_time')
def lucy_time():
    return render_template('weekly.html',weeks=get_date_sequence(Day_Of_Week.TUESDAY), title='Lucy Time', background='dalle - snow playing.png')
    
# Seasonal
app.add_url_rule('/family_game_night','family_game_night',
                 build_weekly(dates, 'Family Game Night!',Day_Of_Week.SUNDAY,'pegs and a die.jpg'))
app.add_url_rule('/dnd','dnd',build_icon_list('Dungeons and Dragons Campaign',10,'d20.png'))

# Exercise
app.add_url_rule('/core','core', build_core(dates, Day_Of_Week.TUESDAY))
app.add_url_rule('/running','running', build_running(dates, [Day_Of_Week.MONDAY, Day_Of_Week.FRIDAY], miles=4.5, minutes=45))

# Lastly the filler.
app.add_url_rule('/notes','notes', build_notes())



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
