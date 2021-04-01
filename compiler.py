from weasyprint import HTML, CSS
import requests

pages = ['daily_planner','weekly_planner','projects','prodev','drawing','spring_goals','movies',
         'disc','bitcoin','running','crypto_investing','bible_mem','hospitality','misc_goals',
         'yearly_goals','video_games','board_games','camping','themes','archery','body_fat',
         'notes','cover']

#page = 

pages = [('cover',0,'portrait'), ('yearly_goals',1,'portrait'), ('daily_planner',2,'landscape')]

for page in pages:
    r = requests.get(f'http://localhost:5000/{page[0]}')
    print(page)
    outs = HTML(string=r.text).write_pdf(f'/tmp/{page[1]} - {page[0]}.pdf',stylesheets=[CSS(string='@page {size: ' + page[2] + '}')])


"""

The idea for this script is to request each page one by one getting the html for the pages. Once I have all the pages then I can convert them into pdfs. I will also be managing the collation here. This script will be hard coded with a set of pages, that list will include whether the page is landscape or portrait and its location in the journal. The script will then take care of collating those pages on to the sheets so that the folios print properly, I'm going to limit myself to folios of 2-3 pages.

Since I don't yet know how to do the collation into pdfs my plan at this point is to just put the pages in the proper order so that if I should have to load them onto a page manually I just do one page then the next then the next and I don't have to think about it. 

Remember, the colation is 4 1 2 3.

The final peice I need to figure out is how to merge two pages into one page so far as the pdf understands it. After I accomplish that it is a simple matter of concatenating.

page = HTML(string=html).write_pdf('/tmp/test.pdf',stylesheets=[CSS(string='@page {size: landscape}')])

"""
