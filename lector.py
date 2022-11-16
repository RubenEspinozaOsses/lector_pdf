import tabula
from PyPDF2 import PdfReader
import pandas as pd
import os
import re


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

def get_name_folder(data):

    for line in data[0]:
        if line.startswith('Nombre') and ':' in line:
            nombre = line.split(': ')[1]
        if line.startswith('RUT') and ':' in line:
            rut = line.split(': ')[1]
        
    return nombre, rut


def extract_raw_data(pdf):
    reader = PdfReader(pdf)
    data = []

    for page_num, page in enumerate(reader.pages):

        text = page.extract_text()
        data.append(text.split('\n'))

    return data
        


def parse_table_data_f1(data):
    table_data = []
    name, rut = get_name_folder(data)
    for num, page in enumerate(data):

        tw_separator = False

        if num == 1:
            label = page[1]
        else:
            label = page[0]

        month, quota = ' '.join(label.split(' ')[0:2]), ''.join(label.split(' ')[2:])

        for line in page:
            if tw_separator:
                line_data = line.split(' ')
                code = line_data[0]
                description = ' '.join(line_data[1:-1])
                value = line_data[-1]
                table_data.append([code, name, rut, description, value, month, quota, (num + 1)])
            if line == 'Código Glosa Valor':
                tw_separator = True
        
            

    return table_data

def parse_table_data_f2(data):
    for num, page in enumerate(data):
        print(f'||||||[{num + 1}]||||||')
        for line in page:
            print(line)



#get_name_folder(extract_raw_data('files/4.pdf'))

data = parse_table_data_f1(extract_raw_data('files/2.pdf'))

final_extracted_data = [line for line in data if re.match('\d', line[0]) and not re.match('/', line[0])]

for line in final_extracted_data:
    print(line)