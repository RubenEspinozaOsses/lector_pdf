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
        


#def parse_table_data_monthly(data):
#    'Parses monthly data from a monthly table into a readable array'
#    table_data = []
#    name, rut = get_name_folder(data)
#    for num, page in enumerate(data):
#
#        tw_separator = False
#
#        if num == 1:
#            label = page[1]
#        else:
#            label = page[0]
#
#        month, quota = ' '.join(label.split(' ')[0:2]), ''.join(label.split(' ')[2:])
#
#        for line in page:
#            if tw_separator:
#                line_data = line.split(' ')
#                code = ''.join([char for char in line_data[0] if char.isdigit()])
#                extra = [char for char in line_data[0] if not char.isdigit()]
#                description = ''.join(extra) + ' '.join(line_data[1:-1])
#                value = line_data[-1]
#                table_data.append(['MENSUAL', code, name, rut, description, value, month, quota, (num + 1)])
#            if line == 'Código Glosa Valor':
#                tw_separator = True
#    
#    to_append = parse_table_data_yearly(data, table_data[-1][-1])
#    for el in to_append:
#        table_data.append(el)
#
#    return table_data
#
#
#
#
#def parse_table_data_yearly(data, start = 0):
#    'Parses data from a yearly table into a readable array'
#    name, rut = get_name_folder(data)
#    table_data = []
#    for i in range(start,len(data)):
#        for index,line in enumerate(data[i]):
#            if line[0].isdigit():
#                year = data[i][1][:19] if i + 1 == 2 else data[i][0][:19]
#                quota = data[i][1][20:] if i + 1 == 2 else data[i][0][20:]
#                label = 'ANUAL'
#                page = i
#                
#                multiple_lines = [data[i][index]]
#                
#                m_idx = index
#                while m_idx + 1 != len(data[i]) and not data[i][m_idx + 1][0].isdigit():
#                    multiple_lines.append(data[i][m_idx + 1])
#                    m_idx += 1
#                description = ''.join(multiple_lines)
#                to_return = [label, description, name, rut, year, quota, page]
#                table_data.append(to_return)
#    return table_data
    

            
def encontrar_datos_codigos(documento_carperta_tributaria):
    codigos_carpeta = ['529', '538', '020', '142', '732', '715', '587', '720']
    datos_de_codigos_encontrados = []
    for numero_pagina, pagina_documento in enumerate(documento_carperta_tributaria):
        if numero_pagina == 1:
            label = pagina_documento[1]
        else:
            label = pagina_documento[0]

        mes_carpeta = ' '.join(label.split(' ')[0:2]).split(' ')
        for linea_documento in pagina_documento:
            for code in codigos_carpeta:
                if code == linea_documento.split(' ')[0]:
                    datos_de_codigos_encontrados.append({code: linea_documento.split(' ')[-1], 'mes': mes_carpeta[0], 'año': mes_carpeta[1] })
    return datos_de_codigos_encontrados
                 
#
def obtener_datos_identificadores(primera_pagina_carpeta, dato_a_buscar):
    for linea_documento in primera_pagina_carpeta:
        if dato_a_buscar in linea_documento:
            return linea_documento.split(dato_a_buscar + ':')[1]
        


def recopilar_datos_carpeta(pdf):
    pdf_as_data = extract_raw_data(pdf)
    nombre_empresario = obtener_datos_identificadores(pdf_as_data[0], 'Nombre del emisor')
    rut_empresario = obtener_datos_identificadores(pdf_as_data[0], 'RUT del emisor')

    
    if identify_format(get_title_of_pdf(pdf)) != 3:
        datos_codigo = encontrar_datos_codigos(pdf_as_data)
    else:
        datos_codigo = []

    datos_contribuyente = {'nombre empresario': nombre_empresario, 'rut empresario': rut_empresario}
    return  datos_codigo, datos_contribuyente


#            
#            
#    
#        
#def process_folders():
#    files = [file for file in os.listdir('files/por_procesar') if file.endswith('.pdf')]
#    processed = []
#    
#    for file in files:
#        archivo_pdf = f'files/por_procesar/{file}'
#        if identify_format(get_title_of_pdf(archivo_pdf)) != 3:
#            processed.append(parse_table_data_monthly(extract_raw_data(archivo_pdf)))
#        else:
#            processed.append(parse_table_data_yearly(extract_raw_data(archivo_pdf)))
#
#    
#    return json.dumps(processed)
#
#def append_new_data(new_data, old_data):
#    for data in new_data:
#        old_data.append(data)
#    return old_data
#
#def append_processed_data(new_json):
#    moment=time.strftime("%Y-%b-%d__%H_%M_%S",time.localtime())
#    with open(f'files/procesado/{moment}.json', 'w+') as out:
#        out.write(new_json)
#        
#
#
#
#print(parse_table_data_monthly(extract_raw_data('files/por_procesar/1.pdf')))
#append_processed_data(process_folders())
print('Finished')
print(recopilar_datos_carpeta('files/por_procesar/4.pdf'))



