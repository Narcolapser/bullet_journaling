def render_pixels():
    emotions = ['Happy','Fun','Relaxed','Productive','Tired','Sad','Anxious']
    sdate1 = datetime.strptime('2024-04-01', '%Y-%m-%d')
    sdate2 = datetime.strptime('2024-08-01', '%Y-%m-%d')
    sdate3 = datetime.strptime('2024-12-01', '%Y-%m-%d')

    fdate1 = datetime.strptime('2024-07-31', '%Y-%m-%d')
    fdate2 = datetime.strptime('2024-11-30', '%Y-%m-%d')
    fdate3 = datetime.strptime('2025-03-31', '%Y-%m-%d')
    
    col1 = get_specific_multi_date_sequence([Day_Of_Week.SUNDAY,Day_Of_Week.MONDAY,Day_Of_Week.TUESDAY,Day_Of_Week.WEDNESDAY,Day_Of_Week.THURSDAY,Day_Of_Week.FRIDAY,Day_Of_Week.SATURDAY], sdate1, fdate1)
    col2 = get_specific_multi_date_sequence([Day_Of_Week.SUNDAY,Day_Of_Week.MONDAY,Day_Of_Week.TUESDAY,Day_Of_Week.WEDNESDAY,Day_Of_Week.THURSDAY,Day_Of_Week.FRIDAY,Day_Of_Week.SATURDAY], sdate2, fdate2)
    col3 = get_specific_multi_date_sequence([Day_Of_Week.SUNDAY,Day_Of_Week.MONDAY,Day_Of_Week.TUESDAY,Day_Of_Week.WEDNESDAY,Day_Of_Week.THURSDAY,Day_Of_Week.FRIDAY,Day_Of_Week.SATURDAY], sdate3, fdate3)
    cols = [col1, col2, col3]
    
    collections = []
    
    for col in cols:
        # Can't use a set because sets are unordered.
        months = []
        for date in col:
            month = date.strftime('%B')
            if month not in months:
                months.append(month)
            if len(months) == 4:
                break

        # Pad the months to get calendars
        calendars = {month:[] for month in months}
        for date in col:
            month = date.strftime('%B')
            if month not in calendars:
                break

            if len(calendars[month]) == 0:
                day_of_week = int(date.strftime('%w'))
                for pad in range(day_of_week):
                    calendars[month].append('')
            calendars[month].append(date.strftime('%d'))
            
        # Convert the calendars into lists of weeks for the template to render on.
        weeks = {month:[] for month in months}
        for month in calendars:
            dow = 0
            week = []
            for date in calendars[month]:
                week.append(date)
                dow += 1
                if dow == 7:
                    dow = 0
                    weeks[month].append(week)
                    week = []
            if dow != 0:
                # If a month only has 1 week in it, we need to pad the end just to make sure the widths all line up.
                while dow < 7:
                    week.append('')
                    dow += 1
                weeks[month].append(week)
        
        collections.append({'months':months,'weeks':weeks})
    return render_template('pixels_annual.html',collections=collections,emotions=emotions)

def templates():
    return {
    'pixels': render_pixels
}
