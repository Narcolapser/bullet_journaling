from datetime import timedelta as delta
from enum import Enum

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

def get_specific_multi_date_sequence(days_of_week:Day_Of_Week,start,end):
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

def get_multi_date_sequence(days_of_week:Day_Of_Week,dates:StartFinish):
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

def get_heart_range():
    return range(100,180,4)
