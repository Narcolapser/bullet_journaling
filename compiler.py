from io import BytesIO

from PyPDF3 import PdfFileWriter, PdfFileReader
from PyPDF3.pdf import PageObject

#pdbytes = BytesIO(open('0_quarter_goals.pdf','rb').read())

#pdfr = PdfFileReader(pdbytes)
r1 = PdfFileReader(open('0_quarter_goals.pdf', 'rb'))
p1 = r1.getPage(0)

r2 = PdfFileReader(open('3_hospitality.pdf','rb'))
p2 = r2.getPage(0)

p3 = PageObject.createBlankPage(None, 17*72, 11*72)

p3.mergeScaledTranslatedPage(p1, 1, 0, 0)
p3.mergeScaledTranslatedPage(p2, 1, 8.5*72, 0)

pdfw = PdfFileWriter()
pdfw.addPage(p3)
pdfw.write(open('out.pdf','wb'))

