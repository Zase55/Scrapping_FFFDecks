import openpyxl

workbook = openpyxl.Workbook()

def create_excel(title: str):
    sheet = workbook.active
    sheet.title = title
    return sheet

def insert_in_excel(sheet, *args):
    sheet.append([*args])
    
def save_excel(file_name: str):
    output_file = file_name
    workbook.save(output_file)
    print(f"Datos exportados a {output_file}")