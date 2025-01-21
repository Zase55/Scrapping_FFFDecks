from enum import Enum
from bs4.element import Tag

class Heads(Enum):
    Name = "Name"
    Number = "Number"
    Image = "Image"
    Rarity = "Rarity"
    Card_Set = "Set"
    Element = "Element"
    Cost ="Cost"
    Card_Type = "Type"
    Ex_Burst = "Ex Burst"
    Multiplayable = "Multiplayable"
    Job ="Job"
    Categories = "Categories"
    Power ="Power"
    Abilities = "Abilities"
    
def get_property_value(span: Tag):
    property_value: str = span.text
    property_value = property_value.replace("\n", "")
    return property_value.strip()
    
def get_elements_dict(trs, idx, properties: dict):
    elements_tr = trs[idx]
    tds = elements_tr.find_all("td")
    elements_span = tds[1].span.span.find_all("span")
    for element in elements_span:
        properties["Elements"].append(get_property_value(element))
    return properties

def get_jobs_dict(trs, idx, properties: dict):
    jobs_tr = trs[idx]
    tds = jobs_tr.find_all("td")
    jobs_span = get_property_value(tds[1].span).split('/')
    for job in jobs_span:
        properties["Jobs"].append(job)
        
    return properties
    
def get_categories_dict(trs, idx, properties: dict):
    categories_tr = trs[idx]
    tds = categories_tr.find_all("td")
    categories_span = tds[1].span.span.find_all("span")
    for category in categories_span:
        properties["Categories"].append(get_property_value(category))
    return properties

def get_attrs_ability_item(item, item_abilities: dict):
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
            
    return item_abilities

def get_abilities_dict(trs, idx, properties):
    abilities_tr = trs[idx]
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
                
            get_attrs_ability_item(item, item_abilities)

            n_abilities.append(item_abilities)
        
        properties["Abilities"].append(n_abilities)
        
    return properties