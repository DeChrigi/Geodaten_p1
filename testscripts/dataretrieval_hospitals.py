import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://welches-spital.ch"
url = "https://welches-spital.ch/schweiz/"

response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

hospital_names = soup.find_all('p', class_="hosplist blue_click_list")

for  hospital in hospital_names:
    hospital_url_base = hospital.find('a')

    hospital_url = hospital_url_base['href']

    hospital_name = hospital.find('a').get_text()

    response_details = requests.get('https://welches-spital.ch/alle-bewertungen.php?hid=464')

    soup2 = BeautifulSoup(response_details.content, 'html.parser')

    print(soup2)

    break
