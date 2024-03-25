from typing import List
from pages.util import StartFinish, get_multi_date_sequence, get_date_sequence, get_heart_range, Day_Of_Week
from datetime import datetime, timedelta as delta
from flask import render_template

def build_goals(season, theme, why, goals:List[str]):
    def quarter_goals():
        return render_template('goals.html',title=season,goals=goals,subtitle=theme,why_theme=why)
    return quarter_goals

def build_weekly_planner(dates, season, activities):
    def weekly_planner():
        dates = get_date_sequence(Day_Of_Week.SUNDAY, dates)
        return render_template('weekly_planner.html',season=season,activities=activities,weeks=dates)
    return weekly_planner

def build_daily_planner(dates, activities: List[str], season, num_months=3):
    def planner():
        # We later strip off the date and use just the month, so we just need to know that we got to the next month with
        # these sequence of dates not that we got to the first of said month. 
        months = [dates.sdate+delta(days=31*i) for i in range(num_months)]
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

def build_icon_list(title:str, rows: int, background: str):
    def page():
        height_map = {
            21:'20',
            10:'40',
            11:'60'
        }
        return render_template('icon_list.html',title=title,rows=rows,img=background,height=height_map[rows])
    return page

def build_weekly(dates:StartFinish, title: str, day_of_week: Day_Of_Week, background: str):
    def weekly():
        return render_template('weekly.html',
                               weeks=get_date_sequence(day_of_week, dates),
                               title=title,
                               background=background)
    return weekly

def build_notes():
    return build_icon_list('Notes', 21, 'notebook.png')