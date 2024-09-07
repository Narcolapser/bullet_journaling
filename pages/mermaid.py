from flask import render_template
import mermaid
from mermaid.graph import Graph
from pathlib import Path



def build_mermaid_diagram(config: dict):
    '''
    Takes a mermaid diagram and converts it into html to be rendered.
    title: title of the page
    file: name of the file
    root: folder root for this quarter
    '''
    file_path = config['root']+'/'+config['file']
    file_check = Path(file_path)

    if file_check.is_file():
        def handler():
            diagram = Graph('Sequence-diagram', open(file_path).read())
            html = mermaid.Mermaid(diagram)._repr_html_()
            ## This is an aweful hack, forgive me:
            html = html.replace('smngrt','smart')
            return render_template('html.html',title=config['title'],html=html)
        return handler
    else:
        raise Exception(f'Was not able to file a file at {file_path}')
