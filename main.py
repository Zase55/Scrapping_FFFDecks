from selenium import webdriver
from playwright.sync_api import sync_playwright
from utils.beautifulsoup import get_html_content, get_image_detail
from utils.constants import url_base
from bs4.element import Tag
from utils.export_excel import create_excel, insert_in_excel, save_excel
import json


sheet = create_excel()
insert_in_excel(sheet, "Name", "Number", "Image", "Rarity", "Set", "Element", "Cost", "Type", "Ex Burst ", "Multiplayable", "Job", "Power", "Abilities")
        
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    for item in range(1,4):
        url = url_base.format(item)
        soup = get_html_content(page, url, timeout=15000, parser="lxml")
          
        div = soup.find_all("div", {"class": "card-title"})[0]
        h2 = div.span.h2.text
        h3 = div.span.h3.text
        
        image = get_image_detail(soup, "src", lambda image: "https" in image["src"])
        
        properties = {}
              
        div = soup.find_all("div", {"class": "properties-container"})[0]
        all_trs = div.find_all("tr")
        trs = all_trs[:9]
        
        for tr in trs:
            tds = tr.find_all("td")
            property_value: str = tds[1].span.text
            property_value = property_value.replace("\n", "")
            properties[tds[0].span.text.strip()] = property_value.strip()
        
        abilities_tr = all_trs[9]
        abilities_divs = abilities_tr.find_all("span")[1].span.find_all("div", recursive=False)
        properties["Abilities"] = []
        for abilities_div in abilities_divs:
            n_abilities = []
            for item in abilities_div.contents:
                item_abilities = {}
                if item == "\n":
                    continue
                if isinstance(item, Tag):
                    if "src" in item.attrs:
                        if "assets" in item["src"]:
                            item_abilities["img"] = f"https://ffdecks.com/{item['src']}"
                    else:
                        if item.name == 'b':
                            item_abilities["b"] = item.text
                        
                        elif item.name == 'i':
                            item_abilities["i"] = item.text
                        
                        elif item.find("strong"):
                            item_abilities["strong"] = item.text.replace("\n", "").strip()
                else:
                    item_abilities["text"] = str(item).strip()

                n_abilities.append(item_abilities)
            
            properties["Abilities"].append(n_abilities)
        
        insert_in_excel(sheet, h2, h3, image, properties["Rarity"], properties["Set"], properties["Element"], properties["Cost"], properties["Type"], properties["EX Burst"], properties["Multiplayable"], properties["Job"], properties["Power"], json.dumps(properties["Abilities"]))
                
    save_excel()  
    browser.close()
    