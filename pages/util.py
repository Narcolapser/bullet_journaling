from datetime import timedelta as delta, date
from enum import Enum
from typing import List

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