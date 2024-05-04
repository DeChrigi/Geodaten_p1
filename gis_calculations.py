import pandas as pd
from shapely.geometry import Point, Polygon
from shapely.wkb import loads
import DBHandler as db

def calculateOevInHospitalIsochronesZH():
    # Isochronen und Datenpunkte abholen
    df_isochrones = db.retrieveIsochronesHospitalsZH()
    df_points = db.retrieveOevDataFinalZH()
    
    # Erstelle ein leeres DataFrame für die Ergebnisse
    results = []
    
    # Iteriere über jeden Ischrone
    for index, isochrone in df_isochrones.iterrows():
        # Erzeuge ein Polygon aus den isochronen-Koordinaten
        isochrone_polygon = loads(isochrone['geom'], hex=True)

        print("Kalkuliere für Isochrone Index: ", index)
        
        # Zähler für Datenpunkte in diesem Ischrone
        count = 0
        
        # Iteriere über jeden Datenpunkt
        for _, point in df_points.iterrows():
            # Erzeuge einen Punkt aus den geografischen Koordinaten
            point_geom = Point(point['Longitude'], point['Latitude'])
            
            # Überprüfe, ob der Punkt innerhalb des Ischrone liegt
            if point_in_polygon(point_geom, isochrone_polygon):
                count += 1
        
        # Füge das Ergebnis einer Liste hinzu
        results.append({
            'Isochrone': index + 1,
            'Krankenhaus': isochrone['Krankenhaus'],
            'AA_MINS': isochrone['AA_MINS'],
            'Anzahl Datenpunkte': count
        })
    
    # Erzeuge ein DataFrame aus der Liste
    results_df = pd.DataFrame(results)

    # Returniere das DataFrame
    return results_df

def calculateOevInSchoolIsochronesZH():
    # Isochronen und Datenpunkte abholen
    df_isochrones = db.retrieveIsochronesSchoolsZH()
    df_points = db.retrieveOevDataFinalZH()
    
    # Erstelle ein leeres DataFrame für die Ergebnisse
    results = []
    
    # Iteriere über jeden Ischrone
    for index, isochrone in df_isochrones.iterrows():
        # Erzeuge ein Polygon aus den isochronen-Koordinaten
        isochrone_polygon = loads(isochrone['geom'], hex=True)

        print("Kalkuliere für Isochrone Index: ", index)
        
        # Zähler für Datenpunkte in diesem Ischrone
        count = 0
        
        # Iteriere über jeden Datenpunkt
        for _, point in df_points.iterrows():
            # Erzeuge einen Punkt aus den geografischen Koordinaten
            point_geom = Point(point['Longitude'], point['Latitude'])
            
            # Überprüfe, ob der Punkt innerhalb des Ischrone liegt
            if point_in_polygon(point_geom, isochrone_polygon):
                count += 1
        
        # Füge das Ergebnis einer Liste hinzu
        results.append({
            'Isochrone': index + 1,
            'Schulname': isochrone['Schulname'],
            'AA_MINS': isochrone['AA_MINS'],
            'Anzahl Datenpunkte': count
        })
    
    # Erzeuge ein DataFrame aus der Liste
    results_df = pd.DataFrame(results)

    # Returniere das DataFrame
    return results_df

# Funktion zur Überprüfung, ob ein Punkt in einem Polygon liegt
def point_in_polygon(point, polygon):
    return polygon.contains(point)
