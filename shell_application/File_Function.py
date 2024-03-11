"""
This file handles file conversion between the pdf, csv, and JSON formats utilizing the appropriate Python libraries
"""
import pandas as pd
import matplotlib.pyplot as plt
import tabula
import json

import pandas as pd
import matplotlib.pyplot as plt
import tabula
import json


# CSV to PDF
def csv_to_pdf(csv_file_path, pdf_file_path):
    df = pd.read_csv(csv_file_path)
    fig, ax = plt.subplots()
    df.plot(ax=ax)
    fig.savefig(pdf_file_path)


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


# CSV to Text
def csv_to_text(source_file, target_file):
    df = pd.read_csv(source_file)
    df.to_csv(target_file, index=False, sep='\t')


# PDF to Text
def pdf_to_text(source_file, target_file):
    text = tabula.read_pdf(source_file, pages='all', output_format='json')
    with open(target_file, 'w') as f:
        f.write(json.dumps(text))


# Text to PDF
def text_to_pdf(source_file, target_file):
    with open(source_file, 'r') as f:
        text = f.read()
    df = pd.DataFrame([text])
    fig, ax = plt.subplots()
    df.plot(ax=ax)
    fig.savefig(target_file)
