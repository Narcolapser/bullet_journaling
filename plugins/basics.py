from typing import List, Dict, Union
from plugins.util import FULL_WEEK, StartFinish, get_date_sequence, Day_Of_Week, get_month_start_and_end, get_specific_multi_date_sequence, get_multi_date_sequence, get_journal_metadata
from datetime import datetime, timedelta as delta
from flask import render_template

def get_sectional_row_height(num_sections, rows_per_section):
    section_pixels = 50
    total_height = 500
    row_total = total_height - section_pixels*num_sections
    row_height = row_total/(rows_per_section*num_sections)
    return str(max(int(row_height),12))

def render_icon_list(meta, config: dict):
    options = {
        'title': config['title'],
        'icon': config['icon'],
        'background': config['background'] if 'background' in config else '',
        'rows': config['rows'],
        'height': str(600/config['rows']),
        'opacity': '0.3' if 'opacity' not in config else parse_percent(config['opacity'])
    }
    return render_template('icon_list.html', **options)

def render_goals(meta, config):
    return render_template('goals.html',title=meta['season'],goals=config['goals'],subtitle=meta['theme'],why_theme=config['why'])

def render_static_page(meta, page):
    return render_template(page)

def render_weekly(meta, config):
    return render_template('weekly.html',
                            weeks=get_date_sequence(config['day_of_week'], meta['dates']),
                            title=config['title'],
                            background=config['background'])

def render_sectional_icon_list(title: str, section_titles: List[str], rows_per_section: int, icon: str):
    height = get_sectional_row_height(len(section_titles),rows_per_section)
    return render_template('icon_list_sections.html',title=title,rows=rows_per_section, img=icon,height=height,
                        sections=section_titles, background='blank.png')

def render_monthly_recap(meta, config):
    dates = meta['dates']
    # Calculate the difference in months
    months_difference = (dates.fdate.year - dates.sdate.year) * 12 + dates.fdate.month - dates.sdate.month + 1
    months = [(dates.sdate+delta(days=31*i)).strftime('%B') for i in range(months_difference)]
    return render_sectional_icon_list('Monthly Recap',months,7,'notebook.png')

def render_notes(meta, config):
    config = {
        'title': 'Notes',
        'rows': 21,
        'icon': 'notebook.png',
        'background': 'blank.png'
    }
    return render_icon_list(meta, config)

def parse_percent(value):
    """
    Parse a percentage value from a string.
    Accepts formats like '10' or '10%'.
    Returns a float between 0.0 and 1.0.
    Raises ValueError if the input is invalid.
    """
    value = value.strip()
    if value.endswith('%'):
        value = value[:-1].strip()

    try:
        number = float(value)
    except ValueError:
        raise ValueError(f"Invalid percentage value: '{value}'")

    if not (0 <= number <= 100):
        raise ValueError(f"Percentage out of range: {number} (must be between 0 and 100)")

    return number / 100

def render_picture_grid(meta, config):
    options = {
        'title': config['title'],
        'picture': config['picture'],
        'rows': config['rows'],
        'columns': config['columns'],
        'opacity': '1' if 'opacity' not in config else parse_percent(config['opacity'])
    }
    return render_template('picture_grid.html', **options)

def render_table(meta, config):
    return render_template('table.html',title=config['title'],columns=config['columns'],rows=config['row_titles'])

def render_cover(meta, config):
    return render_template('cover.html',year=config['year'],seasons=config['seasons'])

def templates():
    return {
    'icon_list': render_icon_list,
    'weekly': render_weekly,
    'goals': render_goals,
    'static_page': render_static_page,
    'sectional_icon_list': render_sectional_icon_list,
    'monthly_recap': render_monthly_recap,
    'notes': render_notes,
    'cover': render_cover,
    'picture_grid': render_picture_grid,
}