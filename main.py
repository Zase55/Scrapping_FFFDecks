from playwright.sync_api import sync_playwright
from utils.beautifulsoup import get_html_content, get_title_card_detail
from utils.constants import url_base, excel_title, excel_file_name
from utils.export_excel import create_excel, insert_in_excel, save_excel
from utils.scraping_cards import Heads
import json


sheet = create_excel(excel_title)
insert_in_excel(sheet, 
                Heads.Name.value,
                Heads.Number.value,
                Heads.Image.value,
                Heads.Rarity.value,
                Heads.Card_Set.value,
                Heads.Element.value,
                Heads.Cost.value,
                Heads.Card_Type.value,
                Heads.Ex_Burst.value,
                Heads.Multiplayable.value,
                Heads.Job.value,
                Heads.Categories.value,
                Heads.Power.value,
                Heads.Abilities.value)
        
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for item in range(1,101):
        url = url_base.format(item)
        soup = get_html_content(page, url, timeout=12000, parser="lxml")
          
        properties = get_title_card_detail(soup)
                
        insert_in_excel(sheet,
                        properties["Name"],
                        properties["Number"],
                        properties["Image"],
                        properties["Rarity"],
                        properties["Set"],
                        json.dumps(properties["Elements"]),
                        properties["Cost"],
                        properties["Type"],
                        properties["EX Burst"],
                        properties["Multiplayable"],
                        json.dumps(properties["Jobs"]),
                        json.dumps(properties["Categories"]),
                        properties["Power"],
                        json.dumps(properties["Abilities"]))
                
    save_excel(excel_file_name)  
    browser.close()
    