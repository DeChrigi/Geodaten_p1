import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

response_details = requests.get('https://welches-spital.ch/alle-bewertungen.php?hid=464')

soup2 = BeautifulSoup(response_details.content, 'html.parser')

testsoup = soup2.decode()

result = testsoup.find("Adresse")

bunga = testsoup[result:result+40]

print(bunga)