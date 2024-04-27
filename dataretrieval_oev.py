import pandas as pd

def scrapeAllOevReturnAsDf():
    df = pd.read_csv('./oev_haltestellen/Betriebspunkt.csv', encoding='ANSI') 
    return df