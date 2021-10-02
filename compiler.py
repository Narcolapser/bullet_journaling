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
#    p1.rotateCounterClockwise(rot1)
#    pdfw = PdfFileWriter()
#    pdfw.addPage(p1)
#    temp = BytesIO()
#    pdfw.write(temp)
#    r1 = PdfFileReader(f1)

    r2 = PdfFileReader(f2)
    p2 = r2.getPage(0)
    if rot2:
        p2 = p2.rotateCounterClockwise(90)
        
#        pdfw = PdfFileWriter()
#        pdfw.addPage(p2)
#        temp = BytesIO()
#        pdfw.write(temp)
#        r2 = PdfFileReader(temp)
#        p2 = r2.getPage(0)

    outs = PageObject.createBlankPage(None, 17*72, 11*72)
    outs.mergeScaledTranslatedPage(p1, 1, 0, 0)
    outs.mergeScaledTranslatedPage(p2, 1, 8.5*72, 0)
    outs.scaleTo(11*72,8.5*72)
#    outs.rotateCounterClockwise(90)
    return outs

f1 = open('0_quarter_goals.pdf','rb')
f2 = open('3_hospitality.pdf','rb')
#f2 = open('1_daily_planner.pdf','rb')

outs = create_page(f1, f2, True, True)

pdfw = PdfFileWriter()
pdfw.addPage(outs)
pdfw.write(open('out.pdf','wb'))

#pdbytes = BytesIO(open('0_quarter_goals.pdf','rb').read())

#pdfr = PdfFileReader(pdbytes)
#r1 = PdfFileReader(open('0_quarter_goals.pdf', 'rb'))
#p1 = r1.getPage(0)

#r2 = PdfFileReader(open('3_hospitality.pdf','rb'))
#p2 = r2.getPage(0)

#outs = merge_to_page(p1,p2)

#pdfw = PdfFileWriter()
#pdfw.addPage(outs)
#pdfw.write(open('out.pdf','wb'))



#r1 = PdfFileReader(open('1_daily_planner.pdf', 'rb'))
#p1 = r1.getPage(0)
#p1.rotateCounterClockwise(90)
#pdfw = PdfFileWriter()
#pdfw.addPage(p1)
#pdfw.write(open('temp.pdf','wb'))

#r2 = PdfFileReader(open('3_hospitality.pdf','rb'))
#p2 = r2.getPage(0)

#outs = merge_to_page(p1,p2)

#pdfw = PdfFileWriter()
#pdfw.addPage(outs)
#pdfw.write(open('out.pdf','wb'))


