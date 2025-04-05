from plugins.util import get_date_sequence
from datetime import datetime, timedelta as delta
from flask import render_template

def render_weekly_planner(meta, config):
    date_sequence = get_date_sequence('sunday', meta['dates'])
    return render_template('weekly_planner.html',season=meta['season'],activities=meta['weekly_activities'],weeks=date_sequence)

def render_daily_planner(meta, config):
    # We later strip off the date and use just the month, so we just need to know that we got to the next month with
    # these sequence of dates not that we got to the first of said month. 
    months = [meta['dates'].sdate+delta(days=31*i+7) for i in range(meta['dates'].getNumberOfMonths())]
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
    return render_template('daily_planner.html',season=meta['season'], months=months, days=days, activities=meta['activities'])


def templates():
    return {
    'weekly_planner': render_weekly_planner,
    'daily_planner': render_daily_planner
}

def default_pages():
    return ['daily_planner','weekly_planner']