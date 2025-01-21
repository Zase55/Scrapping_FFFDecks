# FFDecks Card Scraper

A Python project for scraping card data from the FFDecks website. This tool extracts detailed information about cards, including their names, descriptions, costs, and more, for further analysis or integration into other tools.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)

## Features

- Scrapes card data from the FFDecks website.
- Extracts details such as:
  - Name
  - Number
  - Image
  - Rarity
  - Set
  - Element
  - Cost
  - Type
  - Ex Burst
  - Multiplayable
  - Job
  - Categories
  - Power
  - Abilities
- Saves data to a EXCEL file or database for easy access and manipulation.
- Handles pagination and dynamic content efficiently.

## Requirements

- Python 3.8+
- You must have 'playwright' knowledge to have the browsers installed.
- Required Python libraries:
  - `playwright`
  - `beautifulsoup4(bs4)`
  - `openpyxl`
  - `json`
  - `typing`

## Structure

  - main.py # Main script for scraping
  - utils   # Container general functions
    - beautifulsoup.py # Get url content and get info from beautifulsoup component
    - constants.py
    - export_excel.py # Functions to export EXCEL file.

## Installation

1. Clone the repository:
  ```bash
   git clone https:github.com/Zase55/Scrapping_FFFDecks
   cd Scrapping_FFFDecks
  ```
2. Run project
  ```bash
   python main.py
  ```

## Result
The results will be displayed in the following column format:
 - Name -> Name of the card
 - Number -> Card number that is made up of the collection and order in it. Some may have 2 because they are reissues.
 - Image -> Link with the url of the image in FFDecks.
 - Rarity -> It may be common, rare, hero or legend.
 - Set -> Collection to which it belongs.
 - Element -> Element to which the card belongs. Some can be multiple elements, so the format has to be in dictionary format.
 - Cost -> Cost of the card.
 - Type -> It can be backup, forward, summon or monster.
 - Ex Burst -> Value of yes or no.
 - Multiplayable -> Value of yes or no.
 - Job -> Job to which the card belongs. Some can be multiple jobs, so the format has to be in dictionary format.
 - Categories -> Category to which the card belongs. Some may be from several categories, so the format has to be in dictionary format.
 - Power -> Card power. Summons don't have. Monsters and backups may or may not have them. The forwards always have.
 - Abilities -> Text with the card's abilities. They can be several and contain keywords or images, which is why the result is saved as a dictionary.

| Name     | Number | Image                                                               | Rarity  | Set    | Element | Cost | Type    | Ex Burst | Multiplayable | Job            | Categories | Power | Abilities                                                                                                                                                                   |
|----------|--------|---------------------------------------------------------------------|---------|--------|---------|------|---------|----------|----------------|----------------|------------|-------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Red Mage | 1-003  | https://storage.googleapis.com/ffdecks-card-images/003.jpg          | Common  | Opus I | ["Fire"]    | 2    | Backup  | no       | yes            | ["Standard Unit"] | ["III"]   | null  | [[{"img": "https://ffdecks.com/assets/fftcg/markup/Fire.png"}, {"strong": "1"}, {"img": "https://ffdecks.com/assets/fftcg/markup/Dull.png"}, {"text": ": Choose 1 Forward. It cannot block this turn."}]] |
| Auron    | 1-001  | https://storage.googleapis.com/ffdecks-card-images/001_480x480.jpg | Hero    | Opus I | ["Fire"]    | 6    | Forward | no       | no             | ["Guardian"]       | ["X"]     | 9000  | [[{"text": "When Auron deals damage to your opponent, you may play 1 Fire Backup from your hand onto the field"}, {"b": "dull"}, {"text": "."}]]                          |

