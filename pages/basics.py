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
        date_sequence = get_date_sequence(Day_Of_Week.SUNDAY, dates)
        return render_template('weekly_planner.html',season=season,activities=activities,weeks=date_sequence)
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

def get_sectional_row_height(num_sections, rows_per_section):
    section_pixels = 50
    total_height = 400
    row_total = total_height - section_pixels*num_sections
    return str(int(row_total/(rows_per_section*num_sections)))


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
    return build_icon_list('Notes', 21, 'notebook.png')