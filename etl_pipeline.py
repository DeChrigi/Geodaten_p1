import DBHandler as db
import pandas as pd
from geopy.geocoders import Nominatim
from pyproj import Proj, transform, Transformer

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
    # CH1903+ / LV95 zu WGS84 Transformation
    transformer = Transformer.from_crs("epsg:2056", "epsg:4326", always_xy=True)

    # Daten aus der Datenbank abrufen
    df = db.retrieveOevDataRaw()

    # Initiale Spalten für Ergebnisse hinzufügen
    df['Latitude'] = None
    df['Longitude'] = None

    # Durchführen der Koordinatentransformation für jeden Datensatz
    for index, row in df.iterrows():
        e, n = row["E"], row["N"]
        lon, lat = transformer.transform(e, n)

        print("Latitude:", lat)
        print("Longitude:", lon)

        df.at[index, "Longitude"] = lon
        df.at[index, "Latitude"] = lat

    # Typkonvertierung der neuen Spalten zu float für korrekte Darstellung und Berechnung
    df["Longitude"] = df["Longitude"].astype(float)
    df["Latitude"] = df["Latitude"].astype(float)

    return df



