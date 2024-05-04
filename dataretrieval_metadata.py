import pandas as pd

def scrapeAllPLZReturnAsDf():
    df = pd.read_csv('./metadaten/Liste-der-PLZ-in-Excel-Karte-Schweiz-Postleitzahlen.csv', encoding='UTF-8', delimiter=';') 
    return df
