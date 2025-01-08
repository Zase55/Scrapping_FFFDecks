import openpyxl

workbook = openpyxl.Workbook()

def create_excel():
    sheet = workbook.active
    sheet.title = "Scraping FFDecks"
    return sheet

def insert_in_excel(sheet, *args):
    sheet.append([*args])
    
def save_excel():
    output_file = "scraping_result.xlsx"
    workbook.save(output_file)
    print(f"Datos exportados a {output_file}")