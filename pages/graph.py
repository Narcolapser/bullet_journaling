from typing import List, Dict, Union
from pages.util import FULL_WEEK, StartFinish, get_date_sequence, Day_Of_Week, get_month_start_and_end, get_specific_multi_date_sequence, get_multi_date_sequence
from datetime import datetime, timedelta as delta
from flask import render_template

def float_range(start, end, steps=20):
    distance = end - start
    step = distance*1.0 / (steps - 1)
    result = []
    i = 0
    while i < end:
        result.append(start+i)
        i += step
    return result

def int_range(start, end, steps=20):
    return [round(i) for i in float_range(start, end, steps)]

GraphUnits = Dict[str, List[Union[str, int]]]

class GraphConfig():
    title: str
    units: GraphUnits
    sequnce: List[Union[str,int]]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

def build_graph(config: GraphConfig):
    def handler():
        return render_template('graph.html',sequence=config.sequnce,title=config.title,units=config.units.keys(),unit_steps=config.units)
    return handler

def build_month_graph(config: dict):
    '''
    This is a convenience wrapper for build graph that creates a graph spanning a month. Expected keys in config are:
    title: The title of the page
    month: integer value for the month in question
    dates: the start and end dates for this quarter to ensure we get the right form of february mostly.
    units: dictionary with a unit name and a dictionary of start and end keys with int or float values. 
        If the values are floats, or the difference between the ints is less than 20 then a float range will be used.
    '''
    graph_config = GraphConfig()
    graph_config.title = config['title']

    units: GraphUnits = {}
    for unit in config['units']:
        start = config['units'][unit]['start']
        end = config['units'][unit]['end']
        if isinstance(start,float) or isinstance(end, float) or end - start < 20:
            units[unit] = float_range(start,end)
        else:
            units[unit] = int_range(start,end)
    graph_config.units = units

    sdate, fdate = get_month_start_and_end(config['month'],config['dates'].sdate.year)
    graph_config.sequnce = [i.day for i in get_specific_multi_date_sequence(FULL_WEEK, sdate, fdate)]
    return build_graph(graph_config)
