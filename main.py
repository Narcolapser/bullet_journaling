import requests
import json
from flask import Flask, render_template, request, send_file
from datetime import datetime, timedelta as delta

from pages.util import Day_Of_Week, get_date_sequence, StartFinish
from pages.exercises import build_core, build_running
from pages.basics import build_notes, build_icon_list, build_weekly, build_daily_planner

app = Flask(__name__)

year = '2024'
season = f'Spring {year}'
dates = StartFinish(datetime.strptime('2024-04-01', '%Y-%m-%d'), datetime.strptime('2024-05-31', '%Y-%m-%d'))

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

activities = ['Quiet Hour', 'Dishes','Exercise','Walk Garden','Update Journal']
app.add_url_rule('/daily_planner','daily_planner',build_daily_planner(dates,activities,season,num_months=2))

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

app.add_url_rule('/couples_bible_study','couples_bible_study',
                 build_weekly(dates, 'Couples Bible Study',Day_Of_Week.SATURDAY,'../bible.png'))

app.add_url_rule('/lucy_time','lucy_time',
                 build_weekly(dates, 'Lucy Time',Day_Of_Week.TUESDAY,'dalle - snow playing.png'))

app.add_url_rule('/house_projects','house_projects',build_icon_list('House Projects',11,'handyman.png'))
app.add_url_rule('/celebrations','celebrations',build_icon_list('Celebrations!',21,'tada.png'))

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
