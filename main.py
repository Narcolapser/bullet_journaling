import requests
import json
from flask import Flask, render_template, request, send_file
from datetime import datetime, timedelta as delta

from pages.util import SATURDAY
from pages.exercises import get_core, get_running

app = Flask(__name__)

year = '2024'
season = f'Spring {year}'

# The first sunday of the quarter
sdate = datetime.strptime('2024-04-01', '%Y-%m-%d')

# The last saturday of the quarter
fdate = datetime.strptime('2024-05-31', '%Y-%m-%d')

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
    dates = get_date_sequence(SUNDAY)
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
    return render_template('weekly.html',weeks=get_date_sequence(SATURDAY), title='Couple\'s Bible Study', background='../bible.png')

@app.route('/house_projects')
def house_projects():
    return render_template('icon_list.html',title='House Projects',rows=11,img='checkedbox.png',height='60', background='handyman.png')

@app.route('/lucy_time')
def lucy_time():
    return render_template('weekly.html',weeks=get_date_sequence(TUESDAY), title='Lucy Time', background='dalle - snow playing.png')
    
# Seasonal
@app.route('/sunday_night_family_time')
def sunday_night_family_time():
    return render_template('weekly.html',weeks=get_date_sequence(SUNDAY),title='Family Activity',background='pegs and a die.jpg')
    
@app.route('/dnd')
def dnd():
    return render_template('icon_list.html',title='Dungeons and Dragons Campaign',rows=10,img='d20.png',height='40')

# Exercise
app.add_url_rule('/core','core',get_core(sdate,fdate))
app.add_url_rule('/running','running',get_running(sdate,fdate))

@app.route('/notes')
def notes():
    return render_template('icon_list.html',title='Notes',rows=21,img='notebook.png',height='20')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
