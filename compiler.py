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

f2 = open('3_hospitality.pdf','rb')
f1 = open('0_quarter_goals.pdf','rb')

outs = create_page(f1, f2, False, False)
pdfw = PdfFileWriter()
pdfw.addPage(outs)
pdfw.write(open('out.pdf','wb'))


f1 = open('2_weekly_planner.pdf','rb')
f2 = open('1_daily_planner.pdf','rb')

outs = create_page(f1, f2, True, True)
pdfw = PdfFileWriter()
pdfw.addPage(outs)
pdfw.write(open('rot.pdf','wb'))
