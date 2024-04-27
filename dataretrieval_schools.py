import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

def scrape_schools(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    schools = soup.find_all('div', class_="card card--space-3")
    scrape_data = []

    for school in schools:
        school_name = school.find('h3', class_='post__title').find('a').get_text().strip()
        school_infos_uncleansed = school.find('p', class_='post__perex').get_text()

        start_index_type = school_infos_uncleansed.find(":") + 2
        end_index_type = school_infos_uncleansed.find(",")
        school_type = school_infos_uncleansed[start_index_type:end_index_type].strip()

        start_index_address = end_index_type + 2
        end_index_address = school_infos_uncleansed.find(",", start_index_address)
        school_address = school_infos_uncleansed[start_index_address:end_index_address].strip()

        start_index_plz = end_index_address + 2
        school_plz = school_infos_uncleansed[start_index_plz:start_index_plz+4]

        start_index_ort = start_index_plz + 4
        match = re.search(r'\n', school_infos_uncleansed[start_index_ort:])
        if match:
            end_index_ort = match.start()
            school_ort = school_infos_uncleansed[start_index_ort:][:end_index_ort].strip()
        else:
            school_ort = 'Unbekannt'

        scrape_data.append([school_name, school_type, school_address, school_plz, school_ort])

    return scrape_data

def scrape_all_schools(base_url):
    all_data = []
    page = 1
    while True:
        url = base_url + f"?p={page}"
        page_data = scrape_schools(url)
        if not page_data:
            break
        all_data.extend(page_data)
        page += 1
    return all_data

def scrape_all_schools_return_asDf():
    # Die URL der Webseite
    base_url = "https://www.schulenschweiz.ch/type/obligatorische-schule/"
    all_schools_data = scrape_all_schools(base_url)

    df = pd.DataFrame(all_schools_data, columns=['Schulname', 'Schultyp', 'Adresse', 'PLZ', 'Ort'])
    return df
