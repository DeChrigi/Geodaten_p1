import DBHandler as db
import pandas as pd
from geopy.geocoders import Nominatim
from pyproj import Proj, transform

geolocator = Nominatim(user_agent="geocoding_hospitals_dechrigi")

def get_coordinates(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        else:
            print(f"Adresse konnte nicht geocodet werden: {address}")
            return (None, None)
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten beim Geocoding der Adresse {address}: {e}")
        return (None, None)

def transformHospitalData():
    # Retrieve Data
    df = db.retrieveHospitalDataRaw()
    print('Length with duplicates: ', len(df))

    # Delete Duplicates but keep first record
    df = df.drop_duplicates()
    print('Length without duplicates: ', len(df))

    # Delete Records with missing PLZ
    df_cleaned = df.query("PLZ != 'Nicht gefunden'")
    
    df_cleaned['Latitude'] = None
    df_cleaned['Longitude'] = None
    print('Length without Missing values: ', len(df_cleaned))

    # Loop durch df_cleaned
    for index, row in df_cleaned.iterrows():
        full_adress = f"{row['Adresse']}, {row['PLZ']} {row['Ort']}, Switzerland"
        print(full_adress)
        
        # Führe das Geocoding durch
        latitude, longitude = get_coordinates(full_adress)
        print("Latitude:", latitude)
        print("Longitude:", longitude)

        # Speichern der Ergebnisse in den neuen Spalten
        df_cleaned.at[index, 'Latitude'] = latitude
        df_cleaned.at[index, 'Longitude'] = longitude

    # Typumwandlungen mit Bereinigung
    df_cleaned = df_cleaned[pd.to_numeric(df_cleaned['PLZ'], errors='coerce').notna()]
    df_cleaned['PLZ'] = df_cleaned['PLZ'].astype(int)
    df_cleaned['Krankenhaus'] = df_cleaned['Krankenhaus'].astype(str)
    df_cleaned['Adresse'] = df_cleaned['Adresse'].astype(str)
    df_cleaned['Ort'] = df_cleaned['Ort'].astype(str)
    df_cleaned['Latitude'] = df_cleaned['Latitude'].astype(float)
    df_cleaned['Longitude'] = df_cleaned['Longitude'].astype(float)

    return df_cleaned

def transformSchoolData():
    # Retrieve Data
    df = db.retrieveSchoolDataRaw()
    print('Length with duplicates: ', len(df))

    # Delete Duplicates but keep first record
    df = df.drop_duplicates()
    print('Length without duplicates: ', len(df))

    # Delete Records with missing PLZ
    df_cleaned = df.query("Adresse != '-'")
    df_cleaned['Latitude'] = None
    df_cleaned['Longitude'] = None
    print('Length without Missing values: ', len(df_cleaned))

    # Loop durch df_cleaned
    for index, row in df_cleaned.iterrows():
        full_adress = f"{row['Adresse']}, {row['PLZ']} {row['Ort']}, Switzerland"
        print(full_adress)
        
        # Führe das Geocoding durch
        latitude, longitude = get_coordinates(full_adress)
        print("Latitude:", latitude)
        print("Longitude:", longitude)

        # Speichern der Ergebnisse in den neuen Spalten
        df_cleaned.at[index, 'Latitude'] = latitude
        df_cleaned.at[index, 'Longitude'] = longitude

    # Typumwandlungen mit Bereinigung
    df_cleaned = df_cleaned[pd.to_numeric(df_cleaned['PLZ'], errors='coerce').notna()]
    df_cleaned['PLZ'] = df_cleaned['PLZ'].astype(int)
    df_cleaned['Schulname'] = df_cleaned['Schulname'].astype(str)
    df_cleaned['Schultyp'] = df_cleaned['Schulname'].astype(str)
    df_cleaned['Adresse'] = df_cleaned['Adresse'].astype(str)
    df_cleaned['Ort'] = df_cleaned['Ort'].astype(str)
    df_cleaned['Latitude'] = df_cleaned['Latitude'].astype(float)
    df_cleaned['Longitude'] = df_cleaned['Longitude'].astype(float)

    return df_cleaned

def transformOevData():

    # Definiere die Projektionen
    # CH1903/LV03
    proj_ch1903 = Proj('+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 '
                   '+k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel '
                   '+towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs')
    
    # WGS84
    proj_wgs84 = Proj(proj='latlong', datum='WGS84')

    df = db.retrieveOevDataRaw()

    df['Latitude'] = None
    df['Longitude'] = None

    for index, row in df.iterrows():
        e = row["E"]
        n = row["N"]
    
        lon, lat = transform(proj_ch1903, proj_wgs84, e, n)

        print("Latitude:", lat)
        print("Longitude:", lon)

        df.at[index, "Longitude"] = lon
        df.at[index, "Latitude"] = lat

    df["Longitude"] = df["Longitude"].astype(float)
    df["Latitude"] = df["Latitude"].astype(float)

    return df



