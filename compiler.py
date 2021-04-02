from weasyprint import HTML, CSS
import requests

pages = ['daily_planner','weekly_planner','projects','prodev','drawing','spring_goals','movies',
         'disc','bitcoin','running','crypto_investing','bible_mem','hospitality','misc_goals',
         'yearly_goals','video_games','board_games','camping','themes','archery','body_fat',
         'notes','cover']

#page = 

pages = [('cover',0,'portrait'),
         ('yearly_goals',1,'portrait'),
         ('themes', 2,'portrait'),
         ('archery', 3,'portrait'),
         ('camping', 4,'portrait'),
         ('board_games', 5,'portrait'),
         ('video_games', 6,'portrait'), 
         ('body_fat', 7,'portrait'),
         ('spring_goals', 8,'portrait'),
         ('daily_planner',9,'landscape'),
         ('weekly_planner', 10,'landscape'),
         ('hospitality', 11,'portrait'), 
         ('movies', 12,'portrait'),
         ('bible_mem', 13,'portrait'),
         ('drawing', 14,'portrait'),
         ('bitcoin', 15,'portrait'),
         ('crypto_investing', 16,'portrait'),
         ('prodev', 17,'portrait'),
         ('projects', 18,'portrait'),
         ('running', 19,'landscape'),
         ('disc', 20,'portrait'),
         ('misc_goals', 21,'portrait'),
         ('notes', 22,'portrait'),
         ('notes', 23,'portrait')]

for page in pages:
    print(f'Printing {page[0]}')
    r = requests.get(f'http://localhost:5000/{page[0]}')
    outs = HTML(string=r.text).write_pdf(f'./{page[1]}_{page[0]}.pdf',stylesheets=[CSS(string='@page {size: ' + page[2] + '}')])

index = []
folio = []
for page in pages:
    if len(folio) < 4:
        folio.append(f'{page[1]}_{page[0]}.pdf')
    else:
        index.append(folio)
        folio = [f'{page[1]}_{page[0]}.pdf']

nup = 'pdfnup {left} {right} -o f{folio_number}s{sheet_number}.pdf'
for i, folio in enumerate(index):
    print(nup.format(left=folio[3],right=folio[0],folio_number=i,sheet_number=0))
    print(nup.format(left=folio[1],right=folio[2],folio_number=i,sheet_number=1))

"""

The idea for this script is to request each page one by one getting the html for the pages. Once I have all the pages then I can convert them into pdfs. I will also be managing the collation here. This script will be hard coded with a set of pages, that list will include whether the page is landscape or portrait and its location in the journal. The script will then take care of collating those pages on to the sheets so that the folios print properly, I'm going to limit myself to folios of 2-3 pages.

Since I don't yet know how to do the collation into pdfs my plan at this point is to just put the pages in the proper order so that if I should have to load them onto a page manually I just do one page then the next then the next and I don't have to think about it. 

Remember, the colation is 4 1 2 3.

The final peice I need to figure out is how to merge two pages into one page so far as the pdf understands it. After I accomplish that it is a simple matter of concatenating.

page = HTML(string=html).write_pdf('/tmp/test.pdf',stylesheets=[CSS(string='@page {size: landscape}')])

"""