from typing import List
from pages.util import StartFinish, get_multi_date_sequence, get_date_sequence, get_heart_range, Day_Of_Week
from datetime import timedelta as delta
from flask import render_template

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