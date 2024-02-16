"""
This file handles file conversion between the pdf, csv, and JSON formats utilizing the appropriate Python libraries
"""
import pandas as pd
import matplotlib.pyplot as plt
from pdfminer.six import extract_text


# 1. CSV to PDF
def csv_to_pdf(csv_file_path, pdf_file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Create a figure and axes
    fig, ax = plt.subplots()

    # Plot the data on the axes
    df.plot(ax=ax)

    # Save the figure as a PDF file
    fig.savefig(pdf_file_path)


# 2. PDF to CSV
def pdf_to_csv(source_file, target_file):
    # Extract text from the PDF file
    text = extract_text(source_file)

    # Split the text into lines and then split each line into fields
    data = [line.split() for line in text.split('\n') if line]

    # Convert the data to a DataFrame and then save it as a CSV file
    df = pd.DataFrame(data)
    df.to_csv(target_file, index=False)


# 3. CSV to JSON
def csv_to_json(source_file, target_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(source_file)

    # Save the DataFrame as a JSON file
    df.to_json(target_file, orient='records')


# 4. Test to CSV
def text_to_csv(source_file, target_file):
    # Read the text file into a DataFrame
    df = pd.read_csv(source_file, sep='\t')

    # Save the DataFrame as a CSV file
    df.to_csv(target_file, index=False)
