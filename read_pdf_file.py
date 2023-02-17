import re
import os

import PyPDF2


def read_pdf_file(filename: str):
    """
    Read the text content of a PDF file.

    Parameters:
    filename (str): The name of the PDF file to read.

    Returns:
    str: The text content of the PDF file.
    """

    current_dir = os.getcwd()
    with open(filename, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            page_text = page_text.replace('АО «Kaspi Bank», БИК CASPKZKA, www.kaspi.kz', '')
            page_text = re.sub(r' {2,}', ' ', page_text)
            lines = page_text.split('\n')
            for line in lines:
                if re.match(r'^\d{2}\.\d{2}\.\d{2}', line):
                    text += line
                    text += '\n'
        with open(current_dir + '/data/data', 'w', encoding="utf-8") as data:
            data.write(text)
    return 0