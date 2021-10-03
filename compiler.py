from io import BytesIO
import os

from PyPDF3 import PdfFileWriter, PdfFileReader
from PyPDF3.pdf import PageObject

tmp_file = '/tmp/rotpdf.pdf'

def merge_to_page(page1, page2):
    outs = PageObject.createBlankPage(None, 17*72, 11*72)
    outs.mergeScaledTranslatedPage(p1, 1, 0, 0)
    outs.mergeScaledTranslatedPage(p2, 1, 8.5*72, 0)
    outs.scaleTo(11*72,8.5*72)
    outs.rotateCounterClockwise(90)
    return outs

#def create_page(file1, file2, rot1=False, rot2=False):
#    r1 = PdfFileReader(f1)
#    p1 = r1.getPage(0)

#    r2 = PdfFileReader(f2)
#    p2 = r2.getPage(0)
def create_page(p1, p2, rot1=False, rot2=False):
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
    return outs

def build_folio(pages, padding=None):
    if len(pages) > 12:
        raise Exception(f'Cannot collate more than 12 pages, {len(pages)} were provided.')

    collation_patterns = {4:[3,0,1,2], 8:[7,0,1,6,5,2,3,4], 12:[11,0,1,10,9,2,3,8,7,4,5,6]}

    if not padding:
        # If no padding page was provided, create a blank page to pad with.
        padding = ('blank', PageObject.createBlankPage(None, 8.5*72, 11*72), 'landscape')

    # pad out the folio till it is 4, 8, or 12 pages long.
    #while len(pages)%4 != 0:
    while len(pages) not in collation_patterns:
        pages.append(padding)
        print(len(pages))

    collated = [pages[n] for n in collation_patterns[len(pages)]]
    
    joined = []
    for n in range(int(len(collated)/2)):
        page1 = collated[n*2+0]
        # if the width is greater than the height, the document is in landscape and will need to be rotated.
        rot1 = page1['/MediaBox'][2] > page1['/MediaBox'][3]
        
        page2 = collated[n*2+1]
        rot2 = page2['/MediaBox'][2] > page2['/MediaBox'][3]

        joined.append(create_page(page1, page2, rot1, rot2))

    return joined

def compile_journal(directory, pad_path=None, folio_size=8):
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
    print(folios)
    joined_folios = []
    for folio in folios:
        joined_folios.append(build_folio(folio))
    index = PdfFileWriter()
    for folio in joined_folios:
        for page in folio:
            index.addPage(page)
    index.write(open('out.pdf','wb'))

if __name__ == '__main__':
    compile_journal('./')

#f2 = open('3_hospitality.pdf','rb')
#f1 = open('0_quarter_goals.pdf','rb')

#outs = create_page(f1, f2, False, False)
#pdfw = PdfFileWriter()
#pdfw.addPage(outs)
#pdfw.write(open('out.pdf','wb'))


#f1 = open('2_weekly_planner.pdf','rb')
#f2 = open('1_daily_planner.pdf','rb')

#outs = create_page(f1, f2, True, True)
#pdfw = PdfFileWriter()
#pdfw.addPage(outs)
#pdfw.write(open('rot.pdf','wb'))
