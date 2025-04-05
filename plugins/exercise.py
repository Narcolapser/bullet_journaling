from typing import List
from plugins.graph import GraphUnits, build_quarterly_graph
from pages.util import StartFinish, get_multi_date_sequence, get_date_sequence, Day_Of_Week

from flask import render_template

def get_heart_range():
    return {'start':100, 'end':180}

class StrengthExercise:
    def __init__(self, name, lower_limit, upper_limit):
        self.name = name
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit

# core exercises
planking = StrengthExercise('Planking',100,180)
toe_taps = StrengthExercise('90° Toe Taps',150,300)
shoulder_taps = StrengthExercise('Shoulder Taps',60,120)
russian_twist = StrengthExercise('Russian Twist',55,150)
cross_crunches = StrengthExercise('Cross Crunches',150,300)

# arm exercises
chest_press = StrengthExercise('Chest Press', 50, 90)
angel = StrengthExercise('Inverse Snow Angel', 35,75)
bicep_curl = StrengthExercise('Bicep Curl', 28, 60)
tricep_curl = StrengthExercise('Tricep Curl', 28, 60)
bent_over_row = StrengthExercise('Bent Over Row', 28, 60)

strengthExercises = {
    'planking': planking,
    'toe taps': toe_taps,
    'shoulder taps': shoulder_taps,
    'russian twist': russian_twist,
    'cross crunches': cross_crunches,
    'chest press': chest_press,
    'inverse snow angel': angel,
    'bicep curl': bicep_curl,
    'tricep curl': tricep_curl,
    'bent over row': bent_over_row
}

def build_stacked_graph(meta, config):
    dates = meta['dates']
    title = config['title']
    day_of_week = config['day_of_week']
    exercises: List[StrengthExercise] = []
    for exercise in config['exercises']:
        exercises.append(strengthExercises[exercise])

    date_sequence = get_date_sequence(day_of_week,dates)
    items = [exercise.name for exercise in exercises]
    item_bounds = [(exercise.lower_limit, exercise.upper_limit) for exercise in exercises]
    steps = 6
    item_intervals = [int((bound[1]-bound[0])/steps) for bound in item_bounds]
    item_units = []
    for i,bounds in enumerate(item_bounds):
        units = [bounds[1]]
        for j in range(steps-1):
            units.append(bounds[1] - item_intervals[i] * (j+1))
        item_units.append(units)

    return render_template('stacked_graph.html',dates=date_sequence, title=title ,items=items,
        item_units=item_units, steps=steps)

def build_core(meta, config):
    dates = meta['dates']
    days_of_week = config['days_of_week']
    return build_stacked_graph(dates, 'Core Exercises', day_of_week, [
        planking, toe_taps, shoulder_taps, russian_twist, cross_crunches
    ])

def build_body_fat(meta, config):
    months = ['April','May','June','July','August','September','October','November','December','January','February','March']
    return render_template('body_fat.html',year=meta['year'],months=months)

# def build_biking(sdate,fdate):
#     dates = get_multi_date_sequence([Day_Of_Week.MONDAY,Day_Of_Week.WEDNESDAY],sdate,fdate)
#     units = ['BPM','Time']
#     unit_steps = [range(130,170,2), range(30,50,1)]
#     return render_template('graph.html',dates=dates,title='Exercise Bike',units=units,unit_steps=unit_steps)

def build_running(meta, config):
    miles = config['miles'] if 'miles' in config else 2
    minutes = config['minutes'] if 'minutes' in config else 20
    units = {
        'Heart Rate (BPM)': get_heart_range(),
        'Distance (M)': {'start':miles-2,'end':miles},
        'Time (m)': {'start':minutes-20, 'end':minutes}
    }

    graph_config = {
        'title': 'Running',
        'dates': meta['dates'],
        'units': units,
        'days_of_week': config['days_of_week']
    }
    return build_quarterly_graph(meta, graph_config)

def build_biking(meta, config):
    miles = config['miles'] if 'miles' in config else 2
    minutes = config['minutes'] if 'minutes' in config else 20
    units = {
        'Heart Rate (BPM)': get_heart_range(),
        'Distance (M)': {'start':5,'end':12},
        'Time (m)': {'start':minutes-20, 'end':minutes}
    }

    graph_config = {
        'title': 'Biking',
        'dates': config['dates'],
        'units': units,
        'days_of_week': config['days_of_week']
    }
    return build_quarterly_graph(meta, graph_config)


def build_swiming(meta, page):
    dates = meta['dates']
    days_of_week = config['days_of_week']
    date_sequence = get_multi_date_sequence(days_of_week, dates)
    units = ['Heart Rate (BPM)','Laps','Fastest Lap', 'Average Lap']
    lap_range = range(20,40)
    lap_times = range(40,120,int(120/40))
    unit_steps = [get_heart_range(), lap_range,lap_times,lap_times]
    return render_template('graph.html',dates=date_sequence,title='Swimming',units=units,unit_steps=unit_steps)


def templates():
    return {
        'stacked_graph': build_stacked_graph,
        'core': build_core,
        'body_fat': build_body_fat,
        'biking': build_biking,
        'running': build_running,
        'swiming': build_swiming,
    }
