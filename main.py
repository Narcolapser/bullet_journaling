from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from flask import Flask, render_template
from datetime import datetime, timedelta as delta

from pages.util import Day_Of_Week, StartFinish
from pages.exercises import build_core, build_running
from pages.basics import build_goals, build_notes, build_icon_list, build_weekly, build_daily_planner, build_weekly_planner, build_monthly_recap

app = Flask(__name__)

quarterly = load(open('./notes/2024/1 spring/quarter.yaml'),Loader=Loader)
dates = StartFinish(quarterly['start'],quarterly['end'])

year = str(dates.sdate.year)
theme = quarterly['theme']
def get_season(date_obj):
    month = date_obj.month
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    else:
        return "Fall"
    
season = f'{get_season(dates.sdate)} {year}'

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
why = quarterly['why']
goals = quarterly['goals']
app.add_url_rule('/quarter_goals','quarter_goals',build_goals(season, theme, why, goals))

activities = quarterly['daily']
app.add_url_rule('/daily_planner','daily_planner',build_daily_planner(dates,activities,season,num_months=2))

weekly_activities = quarterly['weekly']
app.add_url_rule('/weekly_planner','weekly_planner',build_weekly_planner(dates, season, weekly_activities))

app.add_url_rule('/monthly_recap','monthly_recap',build_monthly_recap(dates))

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
