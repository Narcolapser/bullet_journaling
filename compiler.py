import os
#from weasyprint import HTML, CSS
from xhtml2pdf import pisa
import requests

from PyPDF3 import PdfFileWriter, PdfFileReader
from PyPDF3.pdf import PageObject

from fpdf import FPDF

from compiler_pages import pages_raw

class NumberPDF(FPDF):
    def __init__(self, lpage, rpage):
        super(NumberPDF, self).__init__()
        self.lpage = lpage
        self.rpage = rpage

    # Overload Footer
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        if self.lpage:
            self.cell(129, 10, str(self.lpage), 0, 0, 'L')
        if self.rpage:
            self.cell(129, 10, str(self.rpage), 0, 0, 'R')

tmp_file = '/tmp/rotpdf.pdf'

def merge_to_page(page1, page2):
    outs = PageObject.createBlankPage(None, 17*72, 11*72)
    outs.mergeScaledTranslatedPage(page1, 1, 0, 0)
    outs.mergeScaledTranslatedPage(page2, 1, 8.5*72, 0)
    outs.scaleTo(11*72,8.5*72)
    outs.rotateCounterClockwise(90)
    return outs

def create_page(p1, p2, rot1=False, rot2=False, lpage_num=None, rpage_num=None):
    outs = PageObject.createBlankPage(None, 17*72, 11*72)

    if rot1:
        outs.mergeRotatedScaledTranslatedPage(p1, 90, 1, 8.5*72, 0)
    else:
        outs.mergeScaledTranslatedPage(p1, 1, 0, 0)

    if rot2:
        outs.mergeRotatedScaledTranslatedPage(p2, 90, 1, 8.5*72*2, 0)
    else:
        outs.mergeScaledTranslatedPage(p2, 1, 8.5*72, 0)

    outs.scaleTo(11*72,8.5*72)
    outs.rotateCounterClockwise(90)
    
    temp = NumberPDF(lpage_num, rpage_num)
    temp.add_page(orientation='L')
    temp.output('/tmp/pntemp.pdf')
    num_page = PdfFileReader('/tmp/pntemp.pdf').getPage(0)
    outs.mergePage(num_page)
    
    return outs

def build_folio(pages, padding=None, starting_page_number=None):
    assert(len(pages) <= 12)

    collation_patterns = {4:[3,0,1,2], 8:[7,0,1,6,5,2,3,4], 12:[11,0,1,10,9,2,3,8,7,4,5,6]}

    if not padding:
        # If no padding page was provided, create a blank page to pad with.
        #padding = ('blank', PageObject.createBlankPage(None, 8.5*72, 11*72), 'landscape')
        padding = PageObject.createBlankPage(None, 8.5*72, 11*72)

    # pad out the folio till it is 4, 8, or 12 pages long.
    while len(pages) not in collation_patterns and len(pages) <= 12:
        pages.append(padding)
        print(len(pages))
    
    assert(len(pages) <= 12)

    collated = [pages[n] for n in collation_patterns[len(pages)]]
    
    joined = []
    for n in range(int(len(collated)/2)):
        page1 = collated[n*2+0]
        # if the width is greater than the height, the document is in landscape and will need to be rotated.
        print(page1)
        rot1 = page1['/MediaBox'][2] > page1['/MediaBox'][3]
        
        page2 = collated[n*2+1]
        rot2 = page2['/MediaBox'][2] > page2['/MediaBox'][3]

        if starting_page_number:
            lpage = starting_page_number + collation_patterns[len(pages)][n*2+0]
            rpage = starting_page_number + collation_patterns[len(pages)][n*2+1]
            joined.append(create_page(page1, page2, rot1, rot2, lpage, rpage))
        else:
            joined.append(create_page(page1, page2, rot1, rot2))

    return joined

def compile_journal(directory, pad_path=None, folio_size=8, starting_page_num=1):
    pdfs = [f for f in os.listdir(directory) if '.pdf' in f and f[0:2].isdigit()]
    pdfs.sort()
    
    folios = []
    while len(pdfs) > 0:
        folio = []
        for i in range(8):
            path = pdfs.pop(0)
            reader = PdfFileReader(path)
            pdf = reader.getPage(0)
            folio.append(pdf)
            if len(pdfs) == 0:
                break
        folios.append(folio)

    joined_folios = []

    ## The last folio may be shorter than the rest which can throw of the calculations below.
    folio_size = max([len(folio) for folio in folios])

    for i,folio in enumerate(folios):
        offset = 0
        if i == 13:
            offset = -3
        joined_folios.append(build_folio(folio,None,i*folio_size+starting_page_num+offset))
        print(f'finished folio {i}')
    index = PdfFileWriter()
    for folio in joined_folios:
        for page in folio:
            index.addPage(page)
    index.write(open('out.pdf','wb'))

pages = [(i,'portrait') if isinstance(i,str) else i for i in pages_raw]

while len(pages)%4 != 0:
    pages.append(('notes', 'portrait'))

pages = [(page[0],i,page[1] if len(page) > 1 else 'portrait') for i,page in enumerate(pages)]


def print_journal(pages):
    for page in pages:
        print('Printing ./{1:0>2}_{0}.pdf'.format(page[0],page[1]), end='...')
        r = requests.get(f'http://localhost:5000/{page[0]}')
        print(r.status_code)
        #outs = HTML(string=r.text).write_pdf('./{1:0>2}_{0}.pdf'.format(page[0],page[1]),
                                             #stylesheets=[CSS(string='@page {size: ' + page[2] + '}')])
        with open('./{1:0>2}_{0}.pdf'.format(page[0],page[1]), 'wb') as pdf_file:
             pisa.CreatePDF(r.text, dest=pdf_file)


if __name__ == '__main__':
    print_journal(pages)
    compile_journal('./', starting_page_num=49)

