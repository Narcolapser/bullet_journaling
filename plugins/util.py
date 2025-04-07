from datetime import timedelta as delta, date, datetime
from enum import Enum
from typing import List
import os
import re

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

class Day_Of_Week(Enum):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6

FULL_WEEK = [
    Day_Of_Week.SUNDAY,
    Day_Of_Week.MONDAY,
    Day_Of_Week.TUESDAY,
    Day_Of_Week.WEDNESDAY,
    Day_Of_Week.THURSDAY,
    Day_Of_Week.FRIDAY,
    Day_Of_Week.SATURDAY
]

class StartFinish():
    def __init__(self,sdate,fdate):
        self.sdate=sdate
        self.fdate=fdate
    
    def __repr__(self):
        return str({'sdate': self.sdate, 'fdate': self.fdate})

    def getNumberOfMonths(self):
        return (self.fdate.year - self.sdate.year) * 12 + (self.fdate.month - self.sdate.month) + 1

def get_specific_multi_date_sequence(days_of_week:List[Day_Of_Week], start: date, end: date):
    dow_list = [start + delta(days=dow.value) for dow in days_of_week]
    week_delta = delta(days=7)
    dates = []
    while dow_list[0] <= end:
        for i,date in enumerate(dow_list):
            if date > end:
                break
            dates.append(date)
            dow_list[i] = date + week_delta
    return dates

def get_multi_date_sequence(days_of_week:list[str],dates:StartFinish):
    days_of_week = [getattr(Day_Of_Week,i.upper()) for i in days_of_week]
    return get_specific_multi_date_sequence(days_of_week,dates.sdate,dates.fdate)

def get_date_sequence(day_string:str ,dates:StartFinish):
    dow = getattr(Day_Of_Week,day_string.upper())
    date = dates.sdate + delta(days=dow.value)
    week_delta = delta(days=7)
    date_sequence = []
    while date <= dates.fdate:
        date_sequence.append(date)
        date = date + week_delta
    return date_sequence

def get_month_start_and_end(month: int, year: int):
    # First day of the month
    start_date = date(year, month, 1)
    
    # Calculate the last day of the month
    if month == 12:
        # If it's December, the next month is January of the next year
        next_month = date(year + 1, 1, 1)
    else:
        # Otherwise, it's the 1st of the next month in the same year
        next_month = date(year, month + 1, 1)
    
    # The last day of the current month is one day before the next month's start
    end_date = next_month - delta(days=1)
    
    return start_date, end_date

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

def get_journal_metadata(path_to_yaml):
    quarterly = load(open(path_to_yaml),Loader=Loader)
    dates = StartFinish(quarterly['start'],quarterly['end'])
    year = str(dates.sdate.year)
    return {
        'dates': dates,
        'year': year,
        'season': f'{get_season(dates.sdate)} {year}',
        'theme': quarterly['theme'],
    }

# Journal data class
class Journal:
    def __init__(self, meta, pages):
        self.meta = meta
        self.pages = pages

def load_journal(journal_id):
    # In future: detect storage backend, like from config
    return load_journal_from_yaml(journal_id)

def load_journal_from_yaml(journal_id):
    try:
        year, filename = journal_id.split('_', 1)
        file_path = os.path.join('./notes', year, f"{filename}.yaml")
        with open(file_path) as f:
            data = load(f, Loader=Loader)

        meta = get_journal_metadata(file_path)
        pages = data.get('pages', [])

        return Journal(meta, pages)

    except Exception as e:
        raise RuntimeError(f"Failed to load journal from YAML: {e}")