from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from flask import Flask, render_template

from pages.util import Day_Of_Week, StartFinish
from pages.exercises import build_swiming
from pages.basics import build_goals, build_notes, build_icon_list, build_table, build_weekly, build_daily_planner, build_weekly_planner, build_monthly_recap, build_static_page, build_pixels, build_picture_grid

app = Flask(__name__)

quarterly = load(open('./notes/2024/2 summer/quarter.yaml'),Loader=Loader)
yearly = load(open('./notes/2024/year.yaml'),Loader=Loader)
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
app.add_url_rule('/daily_planner','daily_planner',build_daily_planner(dates,activities,season,num_months=3))

weekly_activities = quarterly['weekly']
app.add_url_rule('/weekly_planner','weekly_planner',build_weekly_planner(dates, season, weekly_activities))

app.add_url_rule('/monthly_recap','monthly_recap',build_monthly_recap(dates))

app.add_url_rule('/couples_bible_study','couples_bible_study',
                 build_weekly(dates, 'Couples Bible Study: Experiencing God Together',Day_Of_Week.SATURDAY,'../bible.png'))

app.add_url_rule('/lucy_time','lucy_time',
                 build_weekly(dates, 'Lucy Time',Day_Of_Week.TUESDAY,'dalle - dad and daughter playing in the pool.png'))

app.add_url_rule('/house_projects','house_projects',build_icon_list('House Projects',11,'checkedbox.png','handyman.png'))
app.add_url_rule('/celebrations','celebrations',build_icon_list('Celebrations!',21,'tada.png'))

# Seasonal
app.add_url_rule('/dnd','dnd',build_icon_list('Dungeons and Dragons Campaign',10,'d20.png'))
app.add_url_rule('/electronics_project','electronics_project',build_icon_list('Eletronics Project', 21, 'notebook.png'))

columns = [('','10'),('Lesson',90)]
rows = [('<img src="http://localhost:5000/static/vegetable academy.png" style="height: 25px;"/>',i) for i in [
    '4.2: Indoor Planting Techniques',
    '4.3: Outdoor Planting Techniques',
    '5.1: Pruning',
    '5.2: Trellising',
    '5.3: Pest Management',
    '5.4: Season Extension',
    '6.1: Harvest Timing',
    '6.2: Harvest Handling',
    '6.3: Curing Storage Crops',
    '7.1: Storage Zones',
    '7.2: Processing Methods',
    '8.1: Eating in Season',
    '8.2: Waste Management'
]]

app.add_url_rule('/seed_to_table','seed_to_table',build_table('Seed to Table',columns,rows))


# Exercise
app.add_url_rule('/swimming','swimming', build_swiming(dates, [Day_Of_Week.TUESDAY, Day_Of_Week.FRIDAY]))
app.add_url_rule('/ultimate','ultimate',
                 build_weekly(dates, 'Ultimate Frisbee',Day_Of_Week.SATURDAY,'ultimate frisbee.png'))

# Lastly the filler.
app.add_url_rule('/notes','notes', build_notes())



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
