from bs4 import BeautifulSoup
from playwright.sync_api import Page
from typing import Callable
from bs4.element import Tag
from utils.scraping_cards import get_elements_dict, get_jobs_dict, get_categories_dict, get_abilities_dict, get_property_value


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

def get_title_card_detail(soup: BeautifulSoup) -> dict:
    properties = {}
    
    div = soup.find_all("div", {"class": "card-title"})[0]
    properties["Name"] = div.span.h2.text
    properties["Number"] = div.span.h3.text
    properties["Image"] = get_image_detail(soup, "src", lambda image: "https" in image["src"])
    
    properties["Elements"] = []
    properties["Jobs"] = []
    properties["Categories"] = []
    properties["Abilities"] = []
              
    div = soup.find_all("div", {"class": "properties-container"})[0]
    all_trs = div.find_all("tr")
    trs = all_trs[:11]
    
    for i,tr in enumerate(trs):
        if i == 2:
            properties = get_elements_dict(all_trs, i, properties)
        elif i == 7:
            properties = get_jobs_dict(all_trs, i, properties)
        elif i == 8:
            properties = get_categories_dict(all_trs, i, properties)
        elif i == 10:
            properties = get_abilities_dict(all_trs, i, properties)
        else:
            tds = tr.find_all("td")
            properties[tds[0].span.text.strip()] = get_property_value(tds[1].span)
                
    return properties
