# This script is not for bullet journals, rather it compiles the normal journal I have been keeping in my obsidian folder
# through out the year.
import os
import markdown
import pdfkit
from PyPDF3 import PdfFileReader, PdfFileWriter

year = 2022
path = '/home/toby/obsidian/Personal/Journal'
month_names = ['01 January','02 February','03 March','04 April','05 May','06 June','07 July','08 August','09 September','10 October','11 November','12 December']
months = [f'{path}/{year}/{month}' for month in month_names[3:]]
months += [f'{path}/{year+1}/{month}' for month in month_names[0:3]]


files = []
for month in months:
    dir_files = os.listdir(month)
    for f in dir_files:
        if f[0:2].isdigit():
            files.append(f'{month}/{f}')
        else:
            print(f)

content = '###'
files.sort()

for f in files:
#    print(f)
    content += open(f).read() + '\n'

content = content.replace('\n\n','\n')

content = content.replace('\n# ','\n#### ')

content = content.replace("\n## Things I'm thankful for","\n\nThings I'm thankful for\n\n")

content = content.replace("\n## Thing I love about Megan","\n\nThing I love about Megan: ")

content = content.replace("\n## Entry","\n\nEntry\n")

open('journal.md','w').write(content)

# Read the contents of journal.md
with open('journal.md', 'r') as f:
    md_content = f.read()


# Convert the markdown content to HTML
html = markdown.markdown(md_content)

css = """
p {
  text-indent: 1em;
  margin-bottom: 0px;
}"""

# Wrap paragraphs in a <div> element and apply CSS rule
## Attempt to tab in the paragraphs
lines = html.split('\n')
out_lines = []
in_entry = False
for line in lines:
    if line == 'Entry':
        in_entry = True
        out_lines.append(line)
        continue
        
    elif line[0:4] == '####':
        in_entry = False
        
    if in_entry == False:
        l2 = line
    else:
        l2 = '' + line
    out_lines.append(l2)

#content = '\n'.join(out_lines)
html = html.replace('<p>', '<div class="text-indent"><p>')
html = html.replace('</p>', '</p></div>')
#css = '<style>.text-indent p { text-indent: 1em; }</style>'
html = css + html

open('journal.html','w').write(html)


# Set the options for pdfkit
options = {
    'page-size': 'Letter',
    'margin-top': '0.5in',
    'margin-right': '0.55in',
    'margin-bottom': '0.55in',
    'margin-left': '0.5in'
}

# Convert the HTML to PDF
pdfkit.from_string(html, 'journal.pdf', options=options)

# Define input and output filenames
input_file = 'journal.pdf'

# Open the input PDF file and read its contents
with open(input_file, 'rb') as file:
    pdf_reader = PdfFileReader(file)

    # Loop over each page in the PDF and save it as a separate file
    for i in range(pdf_reader.getNumPages()):
        # Create a new PDF writer object
        pdf_writer = PdfFileWriter()

        # Add the current page to the writer object
        page = pdf_reader.getPage(i)
        pdf_writer.addPage(page)

        # Define the output filename for the current page
        output_file = f'{i+1:03}_journal_page.pdf'

        # Write the current page to the output file
        with open(output_file, 'wb') as out_file:
            print(output_file)
            pdf_writer.write(out_file)

