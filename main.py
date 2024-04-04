from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from flask import Flask, render_template
from datetime import datetime, timedelta as delta

from pages.util import Day_Of_Week, StartFinish
from pages.exercises import build_core, build_running, build_body_fat
from pages.basics import build_goals, build_notes, build_icon_list, build_sectional_icon_list, build_table, build_weekly, build_daily_planner, build_weekly_planner, build_monthly_recap, build_static_page, build_pixels, build_picture_grid

app = Flask(__name__)

quarterly = load(open('./notes/2024/1 spring/quarter.yaml'),Loader=Loader)
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

# Yearly Pages
app.add_url_rule('/cover','cover',build_static_page('cover.html'))
app.add_url_rule('/yearly_goals','yearly_goals',build_goals('Annual Goals','','',yearly['goals']))
app.add_url_rule('/themes','themes',build_icon_list('Themes',4,'rainbow.png'))
app.add_url_rule('/body_fat','body_fat',build_body_fat('2024'))
app.add_url_rule('/new_games','new_games',build_icon_list('New Video Games',12,'joystick.png'))
app.add_url_rule('/books','books',build_icon_list('Books (P=Paper, A=Audiobook)',25,'book.png'))
app.add_url_rule('/notable_events','notable_events',build_icon_list('Notable Events',12,'calendar.jpg'))
app.add_url_rule('/pixels','pixels',build_pixels())
app.add_url_rule('/community_events','community_events',build_icon_list('Community Events',12,'calendar.jpg'))
app.add_url_rule('/camping_trips','camping_trips',build_icon_list('Camping Trips',6,'tent.png'))
app.add_url_rule('/gigi_time','gigi_time',build_picture_grid('Gigi Time','grandma.webp',4,3))
app.add_url_rule('/call_nathan','call_nathan',build_picture_grid('Call Nathan','phone.jpg',4,3))
app.add_url_rule('/call_brady','call_brady',build_picture_grid('Call Brady','phone.jpg',4,3))
app.add_url_rule('/date_night','date_night',build_picture_grid('Date Night','hearts.gif',4,3))


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
                 build_weekly(dates, 'Couples Bible Study: Experiencing God Together',Day_Of_Week.SATURDAY,'../bible.png'))

app.add_url_rule('/lucy_time','lucy_time',
                 build_weekly(dates, 'Lucy Time',Day_Of_Week.TUESDAY,'playground2.webp'))

app.add_url_rule('/house_projects','house_projects',build_icon_list('House Projects',11,'checkedbox.png','handyman.png'))
app.add_url_rule('/celebrations','celebrations',build_icon_list('Celebrations!',21,'tada.png'))

# Seasonal
app.add_url_rule('/family_game_night','family_game_night',
                 build_weekly(dates, 'Family Game Night!',Day_Of_Week.SUNDAY,'pegs and a die.jpg'))
app.add_url_rule('/dnd','dnd',build_icon_list('Dungeons and Dragons Campaign',10,'d20.png'))
app.add_url_rule('/electronics_project','electronics_project',build_icon_list('Notes', 21, 'notebook.png'))
app.add_url_rule('/sour_dough','sour_dough',
                 build_sectional_icon_list('Sour Dough Experiments', [f'Try {i+1}' for i in range(4)],4,'notebook.png'))

app.add_url_rule('/health_cookie','health_cookie',
                 build_sectional_icon_list('Health Cookie Experiments', [f'Try {i+1}' for i in range(6)],2,'notebook.png'))

columns = [('','10'),('Lesson',90)]
rows = [('<img src="http://localhost:5000/static/vegetable academy.png" style="height: 25px;"/>',i) for i in [
    '1.1: Grower Assessment',
    '1.2: Site Assessment',
    '1.3: Getting In the Zone',
    '2.1: Bed Layout',
    '2.2: Calculating Production',
    '2.3: Garden Planning',
    '2.4: Seed Selection',
    '3.1: Soil Preparation',
    '3.2: Irrigation Systems',
    '3.3: Weed Management',
    '3.4: Supporting Infrastructure',
    '4.1: Your Planting Log',
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
app.add_url_rule('/core','core', build_core(dates, Day_Of_Week.TUESDAY))
app.add_url_rule('/running','running', build_running(dates, [Day_Of_Week.MONDAY, Day_Of_Week.THURSDAY], miles=4.5, minutes=45))
app.add_url_rule('/ultimate','ultimate',
                 build_weekly(dates, 'Ultimate Frisbee',Day_Of_Week.SATURDAY,'ultimate frisbee.png'))

# Lastly the filler.
app.add_url_rule('/notes','notes', build_notes())



if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
