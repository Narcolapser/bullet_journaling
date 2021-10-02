from io import BytesIO

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

def create_page(file1, file2, rot1=False, rot2=False):
    r1 = PdfFileReader(f1)
    p1 = r1.getPage(0)

    r2 = PdfFileReader(f2)
    p2 = r2.getPage(0)
    if rot2:
        p2.rotateCounterClockwise(90)
        
#        pdfw = PdfFileWriter()
#        pdfw.addPage(p2)
#        temp = BytesIO()
#        pdfw.write(temp)
#        r2 = PdfFileReader(temp)
#        p2 = r2.getPage(0)

    outs = PageObject.createBlankPage(None, 17*72, 11*72)
    outs.mergeRotatedScaledTranslatedPage(p1, 90 if rot1 else 0, 1, 0, 0)
    outs.mergeRotatedScaledTranslatedPage(p2, 90 if rot2 else 0, 1, 8.5*72, 0)
    outs.scaleTo(11*72,8.5*72)
    outs.rotateCounterClockwise(90)
    return outs

f1 = open('0_quarter_goals.pdf','rb')
#f2 = open('3_hospitality.pdf','rb')
f2 = open('1_daily_planner.pdf','rb')

outs = create_page(f1, f2, False, True)

pdfw = PdfFileWriter()
pdfw.addPage(outs)
pdfw.write(open('out.pdf','wb'))
