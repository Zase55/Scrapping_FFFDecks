from playwright.sync_api import sync_playwright
from utils.beautifulsoup import get_html_content, get_title_card_detail
from utils.constants import url_base
from utils.export_excel import create_excel, insert_in_excel, save_excel
import json


sheet = create_excel()
insert_in_excel(sheet, "Name", "Number", "Image", "Rarity", "Set", "Element", "Cost", "Type", "Ex Burst ", "Multiplayable", "Job", "Categories", "Power", "Abilities")
        
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for item in range(1,101):
        url = url_base.format(item)
        soup = get_html_content(page, url, timeout=15000, parser="lxml")
          
        properties = get_title_card_detail(soup)
                
        insert_in_excel(sheet,
                        properties["Name"],
                        properties["Number"],
                        properties["Image"],
                        properties["Rarity"],
                        properties["Set"],
                        properties["Element"],
                        properties["Cost"],
                        properties["Type"],
                        properties["EX Burst"],
                        properties["Multiplayable"],
                        properties["Job"],
                        json.dumps(properties["Categories"]),
                        properties["Power"],
                        json.dumps(properties["Abilities"]))
                
    save_excel()  
    browser.close()
    