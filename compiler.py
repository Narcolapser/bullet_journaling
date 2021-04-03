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
         ('drawing', 9,'portrait'),
         ('weekly_planner', 10,'landscape'),
         ('hospitality', 11,'portrait'), 
         ('movies', 12,'portrait'),
         ('bible_mem', 13,'portrait'),
         ('daily_planner',14,'landscape'),
         ('bitcoin', 15,'portrait'),
         ('crypto_investing', 16,'portrait'),
         ('prodev', 17,'portrait'),
         ('projects', 18,'portrait'),
         ('disc', 19,'portrait'),
         ('running', 20,'landscape'),
         ('misc_goals', 21,'portrait'),
         ('notes', 22,'portrait'),
         ('notes', 23,'portrait')]

for page in pages:
    print(f'Printing {page[0]}')
    r = requests.get(f'http://localhost:5000/{page[0]}')
    outs = HTML(string=r.text).write_pdf(f'./{page[1]}_{page[0]}.pdf',stylesheets=[CSS(string='@page {size: ' + page[2] + '}')])

# 1 sheet per folio
# collation_pattern = [3,0,1,2]

# 2 sheets per folio
collation_pattern = [7,0,1,6,5,2,3,4]
pad_page = '22_notes.pdf'

index = []
folio = []
for page in pages:
    if len(folio) < len(collation_pattern):
        folio.append(f'{page[1]}_{page[0]}.pdf')
    else:
        index.append(folio)
        folio = [f'{page[1]}_{page[0]}.pdf']

while len(folio) < len(collation_pattern):
    folio.append(pad_page)

index.append(folio)

docs = []
nup = 'pdfnup --rotateoversize true {left} {right} -o f{folio_number}s{sheet_number}.pdf'
for i, folio in enumerate(index):
    order = [folio[n] for n in collation_pattern]
    pairs = []
    for n in range(int(len(collation_pattern)/2)):
        pairs.append((order[n*2+0], order[n*2+1]))
    
    
    for j, pair in enumerate(pairs):
        docs.append(f'f{i}s{j}.pdf')
        print(nup.format(left=pair[0],right=pair[1],folio_number=i,sheet_number=j))

# Next create the final PDF compiled of all the above
doc_string = ' '.join(docs)
print(f'pdfunite {doc_string} journal.pdf')
print('rm f*.pdf *_*.pdf')

"""

The idea for this script is to request each page one by one getting the html for the pages. Once I have all the pages then I can convert them into pdfs. I will also be managing the collation here. This script will be hard coded with a set of pages, that list will include whether the page is landscape or portrait and its location in the journal. The script will then take care of collating those pages on to the sheets so that the folios print properly, I'm going to limit myself to folios of 2-3 pages.

Since I don't yet know how to do the collation into pdfs my plan at this point is to just put the pages in the proper order so that if I should have to load them onto a page manually I just do one page then the next then the next and I don't have to think about it. 

Remember, the colation is 4 1 2 3.

The final peice I need to figure out is how to merge two pages into one page so far as the pdf understands it. After I accomplish that it is a simple matter of concatenating.

page = HTML(string=html).write_pdf('/tmp/test.pdf',stylesheets=[CSS(string='@page {size: landscape}')])

"""
