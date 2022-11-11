import tabula
import pandas as pd
import os
import matplotlib.pyplot as plt

user_data = [11.138,31.025,165.668,580.295]
glosa_1 = [169.493,37.91,376.808,304.895]
glosa_2 = [167.963,308.72,376.043,574.94]
pago = [377.573,34.85,503.798,426.53]
datos_banco = [506.093,34.85,597.128,575.705]


pdfs = [file for file in os.listdir(os.path.join('files')) if file.endswith('.pdf')]

def extract_datatables(regions, name, idx):
    dir_name = name.split('.')[0]
    if not os.path.exists(f'files/out/{dir_name}'):
        os.mkdir(f'files/out/{dir_name}')
    return tabula.io.read_pdf(f'files/{name}', pages='all', area=regions, output_format='json', stream=True, output_path=f'files/out/{dir_name}/table-{idx}.json')



for index, pdf in enumerate(pdfs):
    user_data_table = extract_datatables(user_data, pdf, index)
    glosa_1_table = extract_datatables(glosa_1, pdf, index)
    glosa_2_table = extract_datatables(glosa_2, pdf, index)
    pago_table = extract_datatables(pago, pdf, index)
    datos_banco_table = extract_datatables(datos_banco, pdf, index)

    
    
    





