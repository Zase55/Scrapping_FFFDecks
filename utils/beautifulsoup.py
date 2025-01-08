from bs4 import BeautifulSoup
from playwright.sync_api import Page
from typing import Callable


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