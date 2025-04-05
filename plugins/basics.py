from typing import List, Dict, Union
from pages.util import FULL_WEEK, StartFinish, get_date_sequence, Day_Of_Week, get_month_start_and_end, get_specific_multi_date_sequence, get_multi_date_sequence, get_journal_metadata
from datetime import datetime, timedelta as delta
from flask import render_template

def config_check(template_name, config, expected):
    for item in expected:
        if item[0] not in config or str(type(config[item[0]]))[8:-2] != item[1]:
            raise Exception(f'{template_name} needs: {item[0]} type {item[1]}')

def get_sectional_row_height(num_sections, rows_per_section):
    section_pixels = 50
    total_height = 500
    row_total = total_height - section_pixels*num_sections
    row_height = row_total/(rows_per_section*num_sections)
    return str(max(int(row_height),12))

def upcast_config(config:dict, config_type: type):
    ret = config_type()
    for key in config:
        setattr(ret,key,config[key])
    return ret

def render_icon_list(config: dict):
    config_check('Icon List',config,[('title','str'),('rows','int'),('icon','str'),('background','str')])
    height = str(600/config['rows'])
    return render_template('icon_list.html',height=height, **config)

class WeeklyConfig:
    dates:StartFinish
    title: str
    day_of_week: str
    background: str

def render_goals(meta):
    return render_template('goals.html',title=meta['season'],goals=meta['goals'],subtitle=meta['theme'],why_theme=meta['why'])

def render_static_page(page):
    return render_template(page)

def render_weekly(config: WeeklyConfig):
    config = upcast_config(config,WeeklyConfig)
    print(config)
    return render_template('weekly.html',
                            weeks=get_date_sequence(config.day_of_week, config.dates),
                            title=config.title,
                            background=config.background)

def render_sectional_icon_list(title: str, section_titles: List[str], rows_per_section: int, icon: str):
    height = get_sectional_row_height(len(section_titles),rows_per_section)
    return render_template('icon_list_sections.html',title=title,rows=rows_per_section, img=icon,height=height,
                        sections=section_titles, background='blank.png')

def render_monthly_recap(meta):
    dates = meta['dates']
    # Calculate the difference in months
    months_difference = (dates.fdate.year - dates.sdate.year) * 12 + dates.fdate.month - dates.sdate.month + 1
    months = [(dates.sdate+delta(days=31*i)).strftime('%B') for i in range(months_difference)]
    return render_sectional_icon_list('Monthly Recap',months,7,'notebook.png')

def render_notes(meta):
    config = {
        'title': 'Notes',
        'rows': 21,
        'icon': 'notebook.png',
        'background': 'blank.png'
    }
    return render_icon_list(config)

def render_picture_grid(title,picture,rows,cols):
    return render_template('picture_grid.html',rows=rows, cols=cols, title=title, picture=picture)

def render_table(title,columns,row_titles):
    return render_template('table.html',title=title,columns=columns,rows=row_titles)

def templates():
    return {
    'icon_list': render_icon_list,
    'weekly': render_weekly,
    'goals': render_goals,
    'static_page': render_static_page,
    'sectional_icon_list': render_sectional_icon_list,
    'monthly_recap': render_monthly_recap,
    'notes': render_notes,
}

def default_pages():
    return ['goals', 'monthly_recap','notes']