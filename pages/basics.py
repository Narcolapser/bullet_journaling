from typing import List
from pages.util import StartFinish, get_date_sequence, Day_Of_Week, get_specific_multi_date_sequence
from datetime import datetime, timedelta as delta
from flask import render_template

def build_goals(season, theme, why, goals:List[str]):
    def quarter_goals():
        return render_template('goals.html',title=season,goals=goals,subtitle=theme,why_theme=why)
    return quarter_goals

def build_static_page(page):
    def render_page():
        return render_template(page)
    return render_page

def build_weekly_planner(dates, season, activities):
    def weekly_planner():
        date_sequence = get_date_sequence('sunday', dates)
        return render_template('weekly_planner.html',season=season,activities=activities,weeks=date_sequence)
    return weekly_planner

def build_daily_planner(dates, activities: List[str], season, num_months=3):
    def planner():
        # We later strip off the date and use just the month, so we just need to know that we got to the next month with
        # these sequence of dates not that we got to the first of said month. 
        months = [dates.sdate+delta(days=31*i+7) for i in range(num_months)]
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
        return render_template('daily_planner.html',season=season, months=months, days=days, activities=activities)
    return planner

def config_check(template_name, config, expected):
    for item in expected:
        if item[0] not in config or str(type(config[item[0]]))[8:-2] != item[1]:
            raise Exception(f'{template_name} needs: {item[0]} type {item[1]}')

def build_icon_list(config: dict):
    config_check('Icon List',config,[('title','str'),('rows','int'),('icon','str'),('background','str')])
    def page():
        height = str(600/config['rows'])
        return render_template('icon_list.html',height=height, **config)
    return page

def upcast_config(config:dict, config_type: type):
    ret = config_type()
    for key in config:
        setattr(ret,key,config[key])
    return ret

class WeeklyConfig:
    dates:StartFinish
    title: str
    day_of_week: str
    background: str

def build_weekly(config: WeeklyConfig):
    config = upcast_config(config,WeeklyConfig)
    def weekly():
        print(config)
        return render_template('weekly.html',
                               weeks=get_date_sequence(config.day_of_week, config.dates),
                               title=config.title,
                               background=config.background)
    return weekly

def get_sectional_row_height(num_sections, rows_per_section):
    section_pixels = 50
    total_height = 500
    row_total = total_height - section_pixels*num_sections
    row_height = row_total/(rows_per_section*num_sections)
    return str(max(int(row_height),12))


def build_sectional_icon_list(title: str, section_titles: List[str], rows_per_section: int, icon: str):
    height = get_sectional_row_height(len(section_titles),rows_per_section)
    def sectional():
        return render_template('icon_list_sections.html',title=title,rows=rows_per_section, img=icon,height=height,
                            sections=section_titles)
    return sectional

def build_monthly_recap(dates):
    # Calculate the difference in months
    months_difference = (dates.fdate.year - dates.sdate.year) * 12 + dates.fdate.month - dates.sdate.month + 1
    months = [(dates.sdate+delta(days=31*i)).strftime('%B') for i in range(months_difference)]
    return build_sectional_icon_list('Monthly Recap',months,7,'notebook.png')

def build_notes():
    config = {
        'title': 'Notes',
        'rows': 21,
        'icon': 'notebook.png',
        'background': ''
    }
    return build_icon_list(config)

def build_pixels():
    def annual_pixels():
        emotions = ['Happy','Fun','Relaxed','Productive','Tired','Sad','Anxious']
        sdate1 = datetime.strptime('2024-04-01', '%Y-%m-%d')
        sdate2 = datetime.strptime('2024-08-01', '%Y-%m-%d')
        sdate3 = datetime.strptime('2024-12-01', '%Y-%m-%d')

        fdate1 = datetime.strptime('2024-07-31', '%Y-%m-%d')
        fdate2 = datetime.strptime('2024-11-30', '%Y-%m-%d')
        fdate3 = datetime.strptime('2025-03-31', '%Y-%m-%d')
        
        col1 = get_specific_multi_date_sequence([Day_Of_Week.SUNDAY,Day_Of_Week.MONDAY,Day_Of_Week.TUESDAY,Day_Of_Week.WEDNESDAY,Day_Of_Week.THURSDAY,Day_Of_Week.FRIDAY,Day_Of_Week.SATURDAY], sdate1, fdate1)
        col2 = get_specific_multi_date_sequence([Day_Of_Week.SUNDAY,Day_Of_Week.MONDAY,Day_Of_Week.TUESDAY,Day_Of_Week.WEDNESDAY,Day_Of_Week.THURSDAY,Day_Of_Week.FRIDAY,Day_Of_Week.SATURDAY], sdate2, fdate2)
        col3 = get_specific_multi_date_sequence([Day_Of_Week.SUNDAY,Day_Of_Week.MONDAY,Day_Of_Week.TUESDAY,Day_Of_Week.WEDNESDAY,Day_Of_Week.THURSDAY,Day_Of_Week.FRIDAY,Day_Of_Week.SATURDAY], sdate3, fdate3)
        cols = [col1, col2, col3]
        
        collections = []
        
        for col in cols:
            # Can't use a set because sets are unordered.
            months = []
            for date in col:
                month = date.strftime('%B')
                if month not in months:
                    months.append(month)
                if len(months) == 4:
                    break

            # Pad the months to get calendars
            calendars = {month:[] for month in months}
            for date in col:
                month = date.strftime('%B')
                if month not in calendars:
                    break

                if len(calendars[month]) == 0:
                    day_of_week = int(date.strftime('%w'))
                    for pad in range(day_of_week):
                        calendars[month].append('')
                calendars[month].append(date.strftime('%d'))
                
            # Convert the calendars into lists of weeks for the template to render on.
            weeks = {month:[] for month in months}
            for month in calendars:
                dow = 0
                week = []
                for date in calendars[month]:
                    week.append(date)
                    dow += 1
                    if dow == 7:
                        dow = 0
                        weeks[month].append(week)
                        week = []
                if dow != 0:
                    # If a month only has 1 week in it, we need to pad the end just to make sure the widths all line up.
                    while dow < 7:
                        week.append('')
                        dow += 1
                    weeks[month].append(week)
            
            collections.append({'months':months,'weeks':weeks})
        return render_template('pixels_annual.html',collections=collections,emotions=emotions)
    return annual_pixels

def build_picture_grid(title,picture,rows,cols):
    def picture_grid():
        return render_template('picture_grid.html',rows=rows, cols=cols, title=title, picture=picture)
    return picture_grid

def build_table(title,columns,row_titles):
    def table():
        return render_template('table.html',title=title,columns=columns,rows=row_titles)
    return table
