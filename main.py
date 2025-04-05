import os
import importlib.util
import pathlib
import re

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from flask import Flask, render_template

from pages.util import Day_Of_Week, StartFinish, get_journal_metadata
from pages.exercises import build_running, build_stacked_graph, build_biking
from pages.basics import build_goals, build_notes, build_icon_list, build_weekly, build_daily_planner, build_weekly_planner, build_monthly_recap, build_pixels, build_picture_grid
from pages.graph import build_month_graph
from pages.mermaid import build_mermaid_diagram

page_templates = {
    'icon_list': build_icon_list,
    'weekly': build_weekly,
    'running': build_running,
    'biking': build_biking,
    'stacked_graph': build_stacked_graph,
    'month_graph': build_month_graph,
    'mermaid': build_mermaid_diagram,
    'icon_list': build_icon_list,
}

app = Flask(__name__)
plugins = []
templates = {}
default_pages = []
quarter_root = './notes/2025/1 spring'

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

def load_plugins():
    plugins = []

    plugins_dir = pathlib.Path(__file__).parent / "plugins"
    class Plugin:
        module = None
        def templates():
            return {}
        def default_pages():
            return []

    for file in plugins_dir.glob("*.py"):
        if file.name == "__init__.py":
            continue

        module_name = file.stem
        spec = importlib.util.spec_from_file_location(module_name, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        plugin_info = Plugin()

        if hasattr(module, "templates"):
            plugin_info.templates = module.templates

        if hasattr(module, "default_pages"):
            plugin_info.default_pages = module.default_pages

        if plugin_info:
            plugin_info.module = module
            plugins.append(plugin_info)

    return plugins
    
@app.route('/')
def root():
    quarterly = load(open(f'{quarter_root}/quarter.yaml'),Loader=Loader)
    pages = []
    for page in quarterly['pages']:
        url = re.sub(r'[^A-Za-z0-9_]', '_', page['title'])
        pages.append(f'/page/{url}')
    for page in default_pages:
        pages.append(f'/page/{page}')
    pages.sort()
    return render_template('index.html',pages=pages)


@app.route('/page/<page_name>')
def page(page_name):
    quarterly = load(open(f'{quarter_root}/quarter.yaml'),Loader=Loader)
    meta = get_journal_metadata(f'{quarter_root}/quarter.yaml')
    page_urls = {}
    for page in quarterly['pages']:
        page_urls[re.sub(r'[^A-Za-z0-9_]', '_', page['title'])] = page

    if page_name in ['goals','daily_planner','weekly_planner','monthly_recap','notes']:
        return templates[page_name](meta)
    elif page_name in page_urls:
        page = page_urls[page_name]
        print(f"For page {page_name} pulling up template: {page_urls[page_name]['template']}")
        return page_templates[page['template']](page)()
    else:
        return '404, page not found'

@app.route('/build_compiler')
def build_compiler():
    quarterly = load(open(f'{quarter_root}/quarter.yaml'),Loader=Loader)
    yearly = load(open('./notes/2025/year.yaml'),Loader=Loader)
    dates = StartFinish(quarterly['start'],quarterly['end'])
    pages_raw = ['quarter_goals']
    pages_raw.append(('daily_planner','landscape'))
    pages_raw.append(('weekly_planner','landscape'))
    pages_raw.append('monthly_recap')

    for page in quarterly['pages']:
        url = re.sub(r'[^A-Za-z0-9_]', '_', page['title'])
        page['dates'] = dates
        page['root'] = quarter_root
        if page['template'] in ['running','month_graph','biking'] or ('landscape' in page and page['landscape']):
            pages_raw.append((url,'landscape'))
        else:
            pages_raw.append(url)

    compiler_directive = ['pages_raw = [']
    for i,page in enumerate(pages_raw):
        if (i+1)%2==0:
            compiler_directive.append('')
        if isinstance(page,str):
            compiler_directive.append(f'\t\'{page}\',')
        else:
            compiler_directive.append(f'\t{page},')
    compiler_directive.append(']')
    open('compiler_pages.py','w').write('\n'.join(compiler_directive))
    return '<br/>'.join(compiler_directive)

if __name__ == '__main__':
    plugins = load_plugins()
    for plugin in plugins:
        plugin_templates = plugin.templates()
        for template in plugin_templates:
            if template in templates:
                print(f'Template collision, {template} is already used. Loading templates from {plugin["module"]}')
                sys.exit(1)
            else:
                templates[template] = plugin_templates[template]

        default_pages += plugin.default_pages()

    app.run(host='0.0.0.0', port = 5000)
