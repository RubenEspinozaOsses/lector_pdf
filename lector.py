import tabula
from PyPDF2 import PdfReader
import pandas as pd
import os


def identify_format(title):
    match title:
        case 'ACREDITAR TAMAÑO EMPRESA':
            return 0

        case 'PERSONALIZADA':
            return 1

        case 'SOLICITAR CRÉDITOS':
            return 2

        case 'ACREDITAR RENTA':
            return 3

def get_title_of_pdf(pdf):
    reader = PdfReader(pdf)
    page = reader.pages[0]
    text = page.extract_text()

    unclean_title = text.split('\n')[1]

    if ' ' in unclean_title:
        return ' '.join(unclean_title.split(' ')[1::])
    else:
        return unclean_title

def get_tables_from_pdf(pdf, regions, page):
    if page == 2: regions = [30, 581, 24, 36]
    return tabula.io.read_pdf(pdf, area=regions, pages=page, stream=True, multiple_tables=False, format='JSON', output_path='1.json')

def extract_data_from_tables(pdf):
    format_code = identify_format(get_title_of_pdf(pdf))
    regions = [30, 581, 12, 24]
    print(get_tables_from_pdf(pdf, regions, 2))
    print(get_tables_from_pdf(pdf, regions, 3))
    


def extract_raw_data(pdf):
    reader = PdfReader(pdf)

    for page_num, page in enumerate(reader.pages):

        text = page.extract_text()
        print(f'|||||||||{page_num}|||||||||')
        print(text.split('\n'))

extract_raw_data('files/1.pdf')