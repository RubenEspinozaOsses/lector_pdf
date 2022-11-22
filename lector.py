import tabula
from PyPDF2 import PdfReader
import pandas as pd
import os
import re
import json


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
    'Monthly data from a yearly table into a readable array'
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
                table_data.append(['MENSUAL', code, name, rut, description, value, month, quota, (num + 1)])
            if line == 'Código Glosa Valor':
                tw_separator = True
    
    parse_table_data_yearly(data, table_data[-1][-1] + 1)        

    return table_data

def parse_table_data_yearly(data, start = 0):
    'Parses data from a yearly table into a readable array'
    name, rut = get_name_folder(data)
    table_data = []
    for i in range(start,len(data)):
        #Iterating through each page of the pdf as an array
        #if data[i][0] == 'Declaraciones de Renta (F22)': data[i][0] = data[i][1]
        #cod 55 = correo electronico
        print(f'|||Pagina {i + 1}|||')
        tw_separator = False
        for line in data[i]:
            print(line)
            if tw_separator:
                year = line[-4:]

                tw_separator = False
            if 'AÑO TRIBUTARIO' in line:
                tw_separator = True
            
            
    
        
def process_folders():
    files = [file for file in os.listdir(os.path.dirname('files/por_procesar')) if file.endswith('.pdf')]
    processed = []

    for file in files:
        if identify_format(get_title_of_pdf(file)) != 3:
            processed.append(parse_table_data_monthly(extract_raw_data(file)))
        else:
            processed.append(parse_table_data_yearly(extract_raw_data(file)))

    
    return json.dumps(processed)


def append_processed_data(new_json):
    with open('files/procesado/out.json', 'a') as out:
        out.write(new_json)



#Works

#data = parse_table_data_monthly(extract_raw_data('files/2.pdf'))
#final_extracted_data = [line for line in data if re.match('\d', line[0]) and not re.match('/', line[0])]
#for line in final_extracted_data:
#    print(line)

data = parse_table_data_yearly(extract_raw_data('files/por_procesar/4.pdf'))



