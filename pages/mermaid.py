from flask import render_template
import mermaid
from mermaid.graph import Graph

def build_mermaid_diagram(config: dict):
    '''
    Takes a mermaid diagram and converts it into html to be rendered.
    title: title of the page
    file: name of the file
    root: folder root for this quarter
    '''
    diagram = Graph(config['diagram_type'], open(config['root']+'/'+config['file']).read())
    html = mermaid.Mermaid(diagram)._repr_html_()
    def handler():
        return render_template('html.html',title=config['title'],html=html)
    return handler
