from pages.util import get_multi_date_sequence, get_date_sequence
from pages.util import SUNDAY, MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY
from datetime import timedelta as delta

from flask import render_template
def get_biking(sdate,fdate):
    def biking():
        dates = get_multi_date_sequence([MONDAY,WEDNESDAY],sdate,fdate)
        units = ['BPM','Time']
        unit_steps = [range(130,170,2), range(30,50,1)]
        return render_template('graph.html',dates=dates,title='Exercise Bike',units=units,unit_steps=unit_steps)
    return biking

def get_core(sdate, fdate):
    def core():
        dates = get_date_sequence(TUESDAY,sdate,fdate)
        items = ['Planking','90° Toe Taps','Shoulder Taps','Russian Twist','Cross Crunches']
        steps = 5
        item_bounds = [[100,180],[150,300],[60,120],[55,150],[150,300]]
        item_intervals = [int((bound[1]-bound[0])/steps) for bound in item_bounds]
        item_units = []
        for i,bounds in enumerate(item_bounds):
            units = [bounds[1]]
            for j in range(steps-1):
                units.append(bounds[1] - item_intervals[i] * (j+1))
            item_units.append(units)
        return render_template('stacked_graph.html',dates=dates,title='Core workout',items=items,
            item_units=item_units, steps=steps)
    return core

def get_running(sdate, fdate):
    def running():
        dates = get_multi_date_sequence([MONDAY,WEDNESDAY],sdate,fdate)
        units = ['Heart Rate (BPM)','Distance (M)','Time (m)']
        unit_steps = [range(100,180,4),[v/10.0 for v in range(25,45)],range(25,45)]
        return render_template('graph.html',dates=dates,title='Running',units=units,unit_steps=unit_steps)
    return running