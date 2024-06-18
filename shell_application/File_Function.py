"""
This file handles file conversion between the pdf, csv, and JSON formats utilizing the appropriate Python libraries
"""
import pandas as pd
import matplotlib.pyplot as plt
import tabula
import json
from reportlab.pdfgen import canvas  #for creating pdf files

# CSV to PDF
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def csv_to_pdf(source_file, target_file):
    # Read the CSV data
    data = pd.read_csv(source_file)

    # Create a figure and a single subplot
    fig, ax = plt.subplots(figsize=(12, 4))

    # Hide axes
    ax.axis('off')

    # Create a table and save it as a PDF
    table = plt.table(cellText=data.values, colLabels=data.columns, cellLoc='center', loc='center')

    # Auto scale the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    # Save the figure to a PDF file
    pdf_pages = PdfPages(target_file)
    pdf_pages.savefig(fig, bbox_inches='tight')
    pdf_pages.close()


# PDF to CSV
def pdf_to_csv(source_file, target_file):
    df = tabula.read_pdf(source_file, pages='all')
    df.to_csv(target_file, index=False)


# CSV to JSON
def csv_to_json(source_file, target_file):
    df = pd.read_csv(source_file)
    df.to_json(target_file, orient='records')


# Text to CSV
def text_to_csv(source_file, target_file):
    df = pd.read_csv(source_file, sep='\t')
    df.to_csv(target_file, index=False)


# JSON to CSV
def json_to_csv(source_file, target_file):
    df = pd.read_json(source_file)
    df.to_csv(target_file, index=False)


# CSV to Text - Working
def csv_to_text(source_file, target_file):
    df = pd.read_csv(source_file)
    df.to_csv(target_file, index=False, sep='\t')


# PDF to Text
def pdf_to_text(source_file, target_file):
    text = tabula.read_pdf(source_file, pages='all', output_format='json')
    with open(target_file, 'w') as f:
        f.write(json.dumps(text))


# Text to PDF
'''
Issues with this conversion
'''


def text_to_pdf(source_file, target_file):
    # Open the source file and read the text
    with open(source_file, 'r') as f:
        text = f.read()

    # Create a new PDF file
    c = canvas.Canvas(target_file)

    # Add the text to the PDF file
    textobject = c.beginText()
    textobject.setTextOrigin(10, 730)
    textobject.setFont("Helvetica", 14)

    lines = text.split('\n')
    for line in lines:
        textobject.textLine(line)

    c.drawText(textobject)
    # Save the PDF file
    c.save()
