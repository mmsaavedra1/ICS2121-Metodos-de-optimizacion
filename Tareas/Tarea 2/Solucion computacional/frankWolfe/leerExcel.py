import openpyxl

def importar_excel():
    excel_document = openpyxl.load_workbook('Tarea2-2020-2.xlsx')
    sheet = excel_document.get_sheet_by_name('DATA')
    multiple_cells = sheet['A1':'A300']

    matriz_Y = list()
    for row in multiple_cells:
        column = list()
        for cell in row:
            column.append(cell.value)
        matriz_Y.append(column)

    multiple_cells = sheet['B1':'BES300']
    matriz_X = list()
    for row in multiple_cells:
        column = list()
        for cell in row:
            column.append(cell.value)
        matriz_X.append(column)
    
    return matriz_X, matriz_Y

if __name__ == "__main__":
    x, y = importar_excel()
    from pprint import pprint
    pprint(y)