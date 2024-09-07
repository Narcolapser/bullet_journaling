from typing import List
from pages.util import StartFinish, get_multi_date_sequence, get_date_sequence, Day_Of_Week

from flask import render_template


def get_heart_range():
    return range(100,180,4)

def build_body_fat(year):
    def body():
        months = ['April','May','June','July','August','September','October','November','December','January','February','March']
        return render_template('body_fat.html',year=year,months=months)
    return body

def get_biking(sdate,fdate):
    def biking():
        dates = get_multi_date_sequence([Day_Of_Week.MONDAY,Day_Of_Week.WEDNESDAY],sdate,fdate)
        units = ['BPM','Time']
        unit_steps = [range(130,170,2), range(30,50,1)]
        return render_template('graph.html',dates=dates,title='Exercise Bike',units=units,unit_steps=unit_steps)
    return biking

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

def build_core(dates, day_of_week):
    return build_stacked_graph(dates, 'Core Exercises', day_of_week, [
        planking, toe_taps, shoulder_taps, russian_twist, cross_crunches
    ])

def build_stacked_graph(config: dict):
    dates = config['dates']
    title = config['title']
    day_of_week = config['day_of_week']
    exercises: List[StrengthExercise] = []
    for exercise in config['exercises']:
        exercises.append(strengthExercises[exercise])

    def handler():
        date_sequence = get_date_sequence(day_of_week,dates)
        items = [exercise.name for exercise in exercises]
        item_bounds = [(exercise.lower_limit, exercise.upper_limit) for exercise in exercises]
        steps = 5
        item_intervals = [int((bound[1]-bound[0])/steps) for bound in item_bounds]
        item_units = []
        for i,bounds in enumerate(item_bounds):
            units = [bounds[1]]
            for j in range(steps-1):
                units.append(bounds[1] - item_intervals[i] * (j+1))
            item_units.append(units)

        return render_template('stacked_graph.html',dates=date_sequence, title=title ,items=items,
            item_units=item_units, steps=steps)
    return handler

def build_running(config: dict):
    miles = config['miles'] if 'miles' in config else 2
    minutes = config['minutes'] if 'minutes' in config else 20
    def running():
        date_sequence = get_multi_date_sequence(config['days_of_week'], config['dates'])
        units = ['Heart Rate (BPM)','Distance (M)','Time (m)']
        distance_range = [v/10.0 for v in range(int(miles*10-20), int(miles*10))]
        time_range = range(minutes-20,minutes)
        unit_steps = [get_heart_range(), distance_range, time_range]
        return render_template('graph.html',dates=date_sequence,title='Running',units=units,unit_steps=unit_steps)
    return running


def build_swiming(dates: StartFinish, days_of_week: List[Day_Of_Week]):
    def swimming():
        date_sequence = get_multi_date_sequence(days_of_week, dates)
        units = ['Heart Rate (BPM)','Laps','Fastest Lap', 'Average Lap']
        lap_range = range(20,40)
        lap_times = range(40,120,int(120/40))
        unit_steps = [get_heart_range(), lap_range,lap_times,lap_times]
        return render_template('graph.html',dates=date_sequence,title='Swimming',units=units,unit_steps=unit_steps)
    return swimming