from yaml import load
import re
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from flask import Flask, render_template

from pages.util import Day_Of_Week, StartFinish
from pages.exercises import build_running, build_stacked_graph
from pages.basics import build_goals, build_notes, build_icon_list, build_weekly, build_daily_planner, build_weekly_planner, build_monthly_recap, build_pixels, build_picture_grid
from pages.graph import build_month_graph
from pages.mermaid import build_mermaid_diagram

page_templates = {
    'icon_list': build_icon_list,
    'weekly': build_weekly,
    'running': build_running,
    'stacked_graph': build_stacked_graph,
    'month_graph': build_month_graph,
    'mermaid': build_mermaid_diagram
}

app = Flask(__name__)
quarter_root = './notes/2024/3 fall'
quarterly = load(open(f'{quarter_root}/quarter.yaml'),Loader=Loader)
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
pages_raw = ['quarter_goals']

activities = quarterly['daily']
app.add_url_rule('/daily_planner','daily_planner',build_daily_planner(dates,activities,season,num_months=4))
pages_raw.append(('daily_planner','landscape'))

weekly_activities = quarterly['weekly']
app.add_url_rule('/weekly_planner','weekly_planner',build_weekly_planner(dates, season, weekly_activities))
pages_raw.append(('weekly_planner','landscape'))

app.add_url_rule('/monthly_recap','monthly_recap',build_monthly_recap(dates))
pages_raw.append('monthly_recap')

for page in quarterly['pages']:
    url = re.sub(r'[^A-Za-z0-9_]', '_', page['title'])
    page['dates'] = dates
    page['root'] = quarter_root
    app.add_url_rule(f'/{url}',url,page_templates[page['template']](page))
    if page['template'] in ['running','month_graph'] or ('landscape' in page and page['landscape']):
        pages_raw.append((url,'landscape'))
    else:
        pages_raw.append(url)

                 
# Manually Generated Pages.


# Exercise
#app.add_url_rule('/ultimate','ultimate',
                 #build_weekly(dates, 'Ultimate Frisbee',Day_Of_Week.SATURDAY,'ultimate frisbee.png'))

# Lastly the filler.
app.add_url_rule('/notes','notes', build_notes())

compiler_directive = ['pages_raw = [']
for i,page in enumerate(pages_raw):
    if (i+1)%2==0:
        compiler_directive.append('')
    if isinstance(page,str):
        compiler_directive.append(f'\t\'{page}\',')
    else:
        compiler_directive.append(f'\t{page},')
compiler_directive.append(']')
open('compiler_pages.py','w').write('\n'.join(compiler_directive))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
