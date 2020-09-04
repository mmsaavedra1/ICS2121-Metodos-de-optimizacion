import openpyxl
from pprint import pprint

def importar_excel():
    excel_document = openpyxl.load_workbook('Datos Tarea 1.xlsx')
    sheet = excel_document.get_sheet_by_name('Hoja2')
    multiple_cells = sheet['C3':'G57']

    matriz_X = list()
    for row in multiple_cells:
        column = list()
        for cell in row:
            column.append(cell.value)
        matriz_X.append(column)

    multiple_cells = sheet['B3':'B57']
    matriz_Y = list()
    for row in multiple_cells:
        column = list()
        for cell in row:
            column.append(cell.value)
        matriz_Y.append(column)
    
    return matriz_X, matriz_Y
