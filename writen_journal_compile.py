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

content = '##'
files.sort()

for f in files:
#    print(f)
    content += open(f).read() + '\n'

while '\n\n' in content:
    content = content.replace('\n\n','\n')

content = content.replace('\n# ','\n### ')
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
<style>
.text-indent {
  text-indent: 2em;
  font-size: 18px;
}
</style>
"""

# Wrap paragraphs in a <div> element and apply CSS rule
## Attempt to tab in the paragraphs
lines = html.split('\n')
out_lines = []
in_entry = False
for line in lines:
    if line == '<p>Entry</p>':
        in_entry = True
        #out_lines.append(line)
        continue
        
    elif line[0:4] == '<h3>':
        in_entry = False
        
    if in_entry == False:
        l2 = line
    else:
        # The entry section starts with a single paragraph tag. And ends with a closing paragraph tag. But the number of
        # lines inside it can vary so we don't know if this line has a p tag or not.
#        if '<p>' not in line:
#            line = '<p>' + line
#        if '</p>' not in line:
#            line = line + '</p>'
# This approach made to much space between the lines.
        # Lets try wrapping the line in a div, which I think creates a line break. 
        line = f'<div class="text-indent">{line.replace("<p>","").replace("</p>","")}</div>'
        l2 = line
    out_lines.append(l2)
html = '\n'.join(out_lines)

#content = '\n'.join(out_lines)
#html = html.replace('<p>', '<div class="text-indent"><p>')
#html = html.replace('</p>', '</p></div>')
#css = '<style>.text-indent div { text-indent: 1em; }</style>'
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

# First clear the existing pdfs:
# Set the directory to the current directory
dir_path = os.getcwd()

# Get a list of all files in the directory
files = os.listdir(dir_path)

# Loop over the files and delete any that end in '.pdf'
for file in files:
    if file.endswith('.pdf'):
        os.remove(os.path.join(dir_path, file))

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

