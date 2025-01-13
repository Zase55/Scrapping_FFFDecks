from bs4 import BeautifulSoup
from playwright.sync_api import Page
from typing import Callable
from bs4.element import Tag


def get_html_content(page: Page, url: str, timeout: int = 10000, parser: str = "html.parser") -> BeautifulSoup:
    page.goto(url)
    page.wait_for_timeout(timeout)
    html = page.content()
    return BeautifulSoup(html, parser )

def get_image_detail(soup: BeautifulSoup, specific_atr: str|None, dynamic_filter: Callable[[BeautifulSoup], bool]|None) -> None:
    images = soup.find_all("img")
    
    for image in images:
        if dynamic_filter and not dynamic_filter(image):
            continue
        
        if specific_atr and specific_atr in image.attrs:
            return image[specific_atr]
        else:
            return image
        
def get_property_value(span: Tag):
    property_value: str = span.text
    property_value = property_value.replace("\n", "")
    return property_value.strip()

def get_title_card_detail(soup: BeautifulSoup) -> dict:
    properties = {}
    
    div = soup.find_all("div", {"class": "card-title"})[0]
    properties["Name"] = div.span.h2.text
    properties["Number"] = div.span.h3.text
    properties["Image"] = get_image_detail(soup, "src", lambda image: "https" in image["src"])
    
    properties["Categories"] = []
    properties["Abilities"] = []
              
    div = soup.find_all("div", {"class": "properties-container"})[0]
    all_trs = div.find_all("tr")
    trs = all_trs[:11]
    
    for i,tr in enumerate(trs):
        if i == 8:
            categories_tr = all_trs[i]
            tds = categories_tr.find_all("td")
            categories_span = tds[1].span.span.find_all("span")
            for category in categories_span:
                properties["Categories"].append(get_property_value(category))
        elif i == 10:
            abilities_tr = all_trs[i]
            abilities_divs = abilities_tr.find_all("span")[1].span.find_all("div", recursive=False)
            for abilities_div in abilities_divs:
                n_abilities = []
                for item in abilities_div.contents:
                    item_abilities = {}
                    if item == "\n":
                        continue
                    if not isinstance(item, Tag):
                        item_abilities["text"] = str(item).strip()
                        n_abilities.append(item_abilities)
                        continue
                        
                    if "src" in item.attrs:
                        if "assets" in item["src"]:
                            item_abilities["img"] = f"https://ffdecks.com/{item['src']}"
                    else:
                        item_value = get_property_value(item)
                        if item.name == 'b':
                            item_abilities["b"] = item_value
                        
                        elif item.name == 'i':
                            item_abilities["i"] = item_value
                        
                        elif item.find("strong"):
                            item_abilities["strong"] = item_value

                    n_abilities.append(item_abilities)
                
                properties["Abilities"].append(n_abilities)
        else:
            tds = tr.find_all("td")
            properties[tds[0].span.text.strip()] = get_property_value(tds[1].span)
                
    return properties
