from yaml import load
import re
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from flask import Flask, render_template

from pages.util import Day_Of_Week, StartFinish
from pages.exercises import build_running, build_stacked_graph, build_biking
from pages.basics import build_goals, build_notes, build_icon_list, build_weekly, build_daily_planner, build_weekly_planner, build_monthly_recap, build_pixels, build_picture_grid
from pages.graph import build_month_graph
from pages.mermaid import build_mermaid_diagram

page_templates = {
    'icon_list': build_icon_list,
    'weekly': build_weekly,
    'running': build_running,
    'biking': build_biking,
    'stacked_graph': build_stacked_graph,
    'month_graph': build_month_graph,
    'mermaid': build_mermaid_diagram,
    'icon_list': build_icon_list,
}

app = Flask(__name__)
quarter_root = './notes/2025/1 spring'

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
    
@app.route('/')
def root():
    pages = []
    for page in quarterly['pages']:
        url = re.sub(r'[^A-Za-z0-9_]', '_', page['title'])
        pages.append(f'/page/{url}')
    for page in ['quarter_goals', 'daily_planner','weekly_planner','monthly_recap','notes']:
        pages.append(f'/page/{page}')
    pages.sort()
    return render_template('index.html',pages=pages)


@app.route('/page/<page_name>')
def page(page_name):
    quarterly = load(open(f'{quarter_root}/quarter.yaml'),Loader=Loader)
    yearly = load(open('./notes/2025/year.yaml'),Loader=Loader)
    dates = StartFinish(quarterly['start'],quarterly['end'])
    weekly_activities = quarterly['weekly']
    activities = quarterly['daily']
    year = str(dates.sdate.year)
    season = f'{get_season(dates.sdate)} {year}'
    theme = quarterly['theme']
    why = quarterly['why']
    goals = quarterly['goals']
    page_urls = {}
    for page in quarterly['pages']:
        page_urls[re.sub(r'[^A-Za-z0-9_]', '_', page['title'])] = page

    if page_name == 'quarter_goals':
        return build_goals(season, theme, why, goals)()
    elif page_name == 'daily_planner':
        return build_daily_planner(dates,activities,season,num_months=2)()
    elif page_name == 'weekly_planner':
        return build_weekly_planner(dates, season, weekly_activities)()
    elif page_name == 'monthly_recap':
        return build_monthly_recap(dates)
    elif page_name == 'notes':
        return build_notes()()
    elif page_name in page_urls:
        page = page_urls[page_name]
        print(f"For page {page_name} pulling up template: {page_urls[page_name]['template']}")
        return page_templates[page['template']](page)()
    else:
        return '404, page not found'

@app.route('/build_compiler')
def build_compiler():
    quarterly = load(open(f'{quarter_root}/quarter.yaml'),Loader=Loader)
    yearly = load(open('./notes/2025/year.yaml'),Loader=Loader)
    dates = StartFinish(quarterly['start'],quarterly['end'])
    pages_raw = ['quarter_goals']
    pages_raw.append(('daily_planner','landscape'))
    pages_raw.append(('weekly_planner','landscape'))
    pages_raw.append('monthly_recap')

    for page in quarterly['pages']:
        url = re.sub(r'[^A-Za-z0-9_]', '_', page['title'])
        page['dates'] = dates
        page['root'] = quarter_root
        if page['template'] in ['running','month_graph','biking'] or ('landscape' in page and page['landscape']):
            pages_raw.append((url,'landscape'))
        else:
            pages_raw.append(url)

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
    return '<br/>'.join(compiler_directive)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000)
