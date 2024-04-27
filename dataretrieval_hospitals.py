import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


def scrape_all_hospitals_return_asDf():
    base_url = "https://welches-spital.ch"
    url = "https://welches-spital.ch/schweiz/"

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    hospital_names = soup.find_all('p', class_="hosplist blue_click_list")

    # Liste für das Speichern der Daten
    data = []

    for hospital in hospital_names:
        hospital_url_base = hospital.find('a')

        if hospital_url_base:
            hospital_url = hospital_url_base['href']
            hospital_name = hospital_url_base.get_text()
            print('Retrieving Hospital: ', hospital_name)
            subsite = base_url + hospital_url

            response_details = requests.get(subsite)
            soupsubsite = BeautifulSoup(response_details.content, 'html.parser')
            soupsubsitestring = str(soupsubsite)

            adressmatch = re.search('Adresse:', soupsubsitestring)

            if adressmatch:
                try:
                    startstring = soupsubsitestring[adressmatch.start():]
                    correctstring = startstring.partition("<li>")[0]

                    adress = correctstring[8:].partition(',')[0].strip()
                    rest = correctstring[8:].partition(',')[2].strip()

                    plz = rest.split(' ')[0] if rest else 'Nicht gefunden'
                    ort = rest.split(' ')[1] if len(rest.split(' ')) > 1 else 'Nicht gefunden'

                    # Daten sammeln
                    data.append({
                        'Krankenhaus': hospital_name,
                        'Adresse': adress,
                        'PLZ': plz,
                        'Ort': ort
                    })

                except IndexError as e:
                    print(f"Fehler bei der Verarbeitung von {hospital_name}: {e}")
                    data.append({
                        'Krankenhaus': hospital_name,
                        'Adresse': 'Nicht gefunden',
                        'PLZ': 'Nicht gefunden',
                        'Ort': 'Nicht gefunden'
                    })
            else:
                print('Adresse Nicht gefunden')
                data.append({
                    'Krankenhaus': hospital_name,
                    'Adresse': 'Nicht gefunden',
                    'PLZ': 'Nicht gefunden',
                    'Ort': 'Nicht gefunden'
                })
        else:
            print(f"Kein Link gefunden für {hospital.get_text()}")

    # Daten in einen DataFrame umwandeln
    df = pd.DataFrame(data)

    return df
