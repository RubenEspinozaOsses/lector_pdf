#!env/Scripts python
import tabula
from PyPDF2 import PdfReader
import pandas as pd
import os
import re
import json
import time


def identify_format(title):
    'Identify the format of a given folder title'
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
    'Gets the title (type of folder) of the PDF file'
    reader = PdfReader(pdf)
    page = reader.pages[0]
    text = page.extract_text()

    unclean_title = text.split('\n')[1]

    if ' ' in unclean_title:
        return ' '.join(unclean_title.split(' ')[1::])
    else:
        return unclean_title

def get_name_folder(data):
    'Get the name of the owner of the folder (pdf) and its rut'
    for line in data[0]:
        if line.startswith('Nombre') and ':' in line:
            nombre = line.split(': ')[1]
        if line.startswith('RUT') and ':' in line:
            rut = line.split(': ')[1]
        
    return nombre, rut


def extract_raw_data(pdf):
    'Extracts the data from the PDF file as plain text, then returns it as a list'
    reader = PdfReader(pdf, strict=True)
    data = []

    for page_num, page in enumerate(reader.pages):

        text = page.extract_text()
        data.append(text.split('\n'))

    return data
        


def parse_table_data_monthly(data):
    'Parses monthly data from a monthly table into a readable array'
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
                code = ''.join([char for char in line_data[0] if char.isdigit()])
                extra = [char for char in line_data[0] if not char.isdigit()]
                description = ''.join(extra) + ' '.join(line_data[1:-1])
                value = line_data[-1]
                table_data.append(['MENSUAL', code, name, rut, description, value, month, quota, (num + 1)])
            if line == 'Código Glosa Valor':
                tw_separator = True
    
    to_append = parse_table_data_yearly(data, table_data[-1][-1])
    for el in to_append:
        table_data.append(el)

    return table_data




def parse_table_data_yearly(data, start = 0):
    'Parses data from a yearly table into a readable array'
    name, rut = get_name_folder(data)
    table_data = []
    for i in range(start,len(data)):
        for index,line in enumerate(data[i]):
            if line[0].isdigit():
                year = data[i][1][:19] if i + 1 == 2 else data[i][0][:19]
                quota = data[i][1][20:] if i + 1 == 2 else data[i][0][20:]
                label = 'ANUAL'
                page = i
                
                multiple_lines = [data[i][index]]
                
                m_idx = index
                while m_idx + 1 != len(data[i]) and not data[i][m_idx + 1][0].isdigit():
                    multiple_lines.append(data[i][m_idx + 1])
                    m_idx += 1
                description = ''.join(multiple_lines)
                to_return = [label, description, name, rut, year, quota, page]
                table_data.append(to_return)
    return table_data
    

            
def find_codes(data):
    lines_wcodes = []
    codes = ['529', '538', '020', '142', '732', '715', '587', '720']


    for page in data:
        for line in page:
            found_codes = []
            for code in codes:
                if code == line.split(' ')[0]:
                    if code not in found_codes:
                        found_codes.append(code)
                    
                    print(line)

def execute(pdf):
    pdf_as_data = extract_raw_data(pdf)
    list_wcodes = find_codes(pdf_as_data)
            
            
    
        
def process_folders():
    files = [file for file in os.listdir('files/por_procesar') if file.endswith('.pdf')]
    processed = []
    
    for file in files:
        archivo_pdf = f'files/por_procesar/{file}'
        if identify_format(get_title_of_pdf(archivo_pdf)) != 3:
            processed.append(parse_table_data_monthly(extract_raw_data(archivo_pdf)))
        else:
            processed.append(parse_table_data_yearly(extract_raw_data(archivo_pdf)))

    
    return json.dumps(processed)

def append_new_data(new_data, old_data):
    for data in new_data:
        old_data.append(data)
    return old_data

def append_processed_data(new_json):
    moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())
    with open(f'files/procesado/{moment}.json', 'w+') as out:
        out.write(new_json)
        



#print(parse_table_data_monthly(extract_raw_data('files/por_procesar/1.pdf')))
#append_processed_data(process_folders())
print('Finished')
execute('files/por_procesar/3.pdf')



