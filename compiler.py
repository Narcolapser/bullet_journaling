from io import BytesIO

from PyPDF3 import PdfFileWriter, PdfFileReader

pdbytes = BytesIO(open('0_quarter_goals.pdf','rb').read())

pdfr = PdfFileReader(pdbytes)
