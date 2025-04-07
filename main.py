import os
import importlib.util
import pathlib
import re

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from flask import Flask, render_template, abort

from plugins.util import load_journal, get_journal_metadata

app = Flask(__name__)
plugins = []
templates = {}
default_pages = []

def load_plugins():
    plugins = []

    plugins_dir = pathlib.Path(__file__).parent / "plugins"
    class Plugin:
        module = None
        def templates(self):
            return {}
        def default_pages(self):
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
    journals = []
    notes_dir = './notes'
    for year in os.listdir(notes_dir):
        year_path = os.path.join(notes_dir, year)
        if os.path.isdir(year_path):
            for file in os.listdir(year_path):
                if file.endswith('.yaml'):
                    journal_id = f"{year}_{os.path.splitext(file)[0]}"
                    journals.append(f'/journal/{journal_id}')
    journals.sort()
    return render_template('index.html', pages=journals)

@app.route('/journal/<journalid>')
def journal(journalid):
    try:
        journal = load_journal(journalid)
    except Exception as e:
        return f"Error loading journal: {e}", 404

    pages = []
    for page in journal.pages:
        url = re.sub(r'[^A-Za-z0-9_]', '_', page['title'])
        pages.append(f'/journal/{journalid}/page/{url}')
    for page in default_pages:
        pages.append(f'/journal/{journalid}/page/{page}')
    pages.sort()

    return render_template('index.html', pages=pages)

@app.route('/journal/<journalid>/page/<page_name>')
def page(journalid, page_name):
    try:
        journal = load_journal(journalid)
    except Exception as e:
        return f"Error loading journal: {e}", 404

    meta = journal.meta
    page_urls = {}

    for page in journal.pages:
        safe_title = re.sub(r'[^A-Za-z0-9_]', '_', page['title'])
        page_urls[safe_title] = page

    for page in default_pages:
        page_urls[re.sub(r'[^A-Za-z0-9_]', '_', page)] = {'template': page}

    if page_name in page_urls:
        page_data = page_urls[page_name]
        print(f"For page {page_name} pulling up template: {page_data['template']}")
        return templates[page_data['template']](meta, page_data)
    else:
        abort(404)


@app.route('/build_compiler')
def build_compiler():
    meta = get_journal_metadata(f'{quarter_root}/quarter.yaml')
    quarterly = load(open(f'{quarter_root}/quarter.yaml'),Loader=Loader)
    yearly = load(open('./notes/2025/year.yaml'),Loader=Loader)
    dates = meta['dates']
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
    
    print('Found the following templates:')
    for template in templates: print(template)

    print('including the following default pages')
    print(default_pages)

    app.run(host='0.0.0.0', port = 5000)
